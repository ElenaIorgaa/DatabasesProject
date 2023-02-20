from flask import Flask, render_template, jsonify, request, redirect, flash
import cx_Oracle
from datetime import datetime

app = Flask(__name__)
with open(app.root_path + '\config.cfg', 'r') as f:
    app.config['ORACLE_URI'] = f.readline()
con = cx_Oracle.connect(user='bd148', password="danuandsa",dsn="bd-dc.cs.tuiasi.ro:1539/orcl")
app.secret_key="hello"

#sali begin code
@app.route('/')
def _logare():
	return render_template('login.html')

@app.route('/logare', methods=['POST'])
def login():
	if request.method == 'POST':
		cur = con.cursor()
		id = request.form['id_user']
		pas=request.form['parola']
		query='select parola from users where id_user=%s'%("'"+id+"'")
		cur.execute(query)
		vals=cur.fetchall()
		print(vals)
		if(len(vals)==0):
			val=None
			print("e nul")

		else:
			val=vals[0][0]
		if(val==pas):
			return redirect('/sali')
		else:
			flash('Utilizator sau parola gresite')
			return redirect('/')




@app.route('/sali')
def _sali():
	sali=[]
	cur=con.cursor()
	cur.execute('select * from sali')
	for result in cur:
		sala={}
		sala['id_sala']=result[0];
		sala['dimensiune']=result[1];
		sala['capacitate']=result[2];
		sali.append(sala)

	cur.close();
	return render_template('sali.html', sali=sali)

@app.route('/grupe')
def _grupe():
	grupe=[]
	cur=con.cursor()
	cur.execute('select * from grupe')
	for result in cur:
		grupa={}
		grupa['id_grupa']=result[0];
		grupa['statut']=result[1];
		grupa['sali_id_sala']=result[2];
		grupe.append(grupa)

	cur.close();
	return render_template('grupe.html', grupe=grupe)

@app.route('/elevi')
def _elevi():
	elevi=[]
	cur=con.cursor()
	cur.execute('select * from elevi')
	for result in cur:
		elev={}
		elev['id_elev']=result[0];
		elev['statut']=result[1];
		elev['nume']=result[2];
		elev['prenume'] = result[3];
		elev['varsta'] = result[4];
		elev['grupe_id_grupa'] = result[5];
		elev['grupe_sali_id_sala'] = result[6];
		elevi.append(elev)
	grupe=[]
	cur.execute('select id_grupa from grupe')
	for result in cur:
		grupe.append(result[0])
	sali=[]
	cur.execute('select id_sala from sali')
	for result in cur:
		sali.append(result[0])
	tupla=[]
	for grupa in grupe:
		query='SELECT sali_id_sala FROM grupe WHERE id_grupa=%s'%(grupa)
		cur.execute(query)
		valos=cur.fetchall()
		vals=valos[0][0]
		list=[]
		list.append(grupa)
		list.append(vals)
		tupla.append(list)
	stats=[]
	cur.execute('select statut from elevi')
	for result in cur:
		stats.append(result[0])

	cur.close();
	return render_template('elevi.html', elevi=elevi, grupe=tupla, sali=sali, stats=stats)

@app.route('/elevi_spect')
def _elevi_spect():
	elevis=[]
	cur=con.cursor()
	cur.execute('select * from elevi_spectacol')
	for result in cur:
		elevs={}
		elevs['elevi_id_elev']=result[0];
		elevs['elevi_id_grupa']=result[1];
		elevs['elevi_id_sala']=result[2];
		elevs['spectacole_id_spectacol'] = result[3];
		elevis.append(elevs)
	grupe=[]
	cur.execute('select id_grupa from grupe')
	for result in cur:
		grupe.append(result[0])
	sali=[]
	cur.execute('select id_sala from sali')
	for result in cur:
		sali.append(result[0])
	tupla = []

	elevi=[]
	cur.execute('select id_elev from elevi')
	for result in cur:
		elevi.append(result[0])

	for elev in elevi:
		query = 'SELECT grupe_id_grupa FROM elevi WHERE id_elev=%s' % (elev)
		query2 = 'SELECT grupe_sali_id_sala FROM elevi WHERE id_elev=%s' % (elev)
		cur.execute(query)
		valos = cur.fetchall()
		print(valos)
		vals = valos[0][0]

		cur.execute(query2)
		valos2=cur.fetchall()
		vals2=valos2[0][0]
		list = []
		list.append(elev)
		list.append(vals)
		list.append(vals2)
		tupla.append(list)

	spectacole=[]
	cur.execute('select id_spectacol from spectacole')
	for result in cur:
		spectacole.append(result[0])

	cur.close();
	return render_template('elevi_spectacol.html',elevi_spectacole=elevis, elevi=tupla, grupe=tupla, sali=sali, spectacole=spectacole)
@app.route('/instructori')
def _instructori():
	instructori=[]
	cur=con.cursor()
	cur.execute('select * from instructori')
	for result in cur:
		instructor={}
		instructor['id_instructor']=result[0];
		instructor['nume']=result[1];
		instructor['prenume'] = result[2];
		instructor['statut']=result[3];
		instructor['experienta'] = result[4];
		instructor['grupe_id_grupa'] = result[5];
		instructor['grupe_sali_id_sala'] = result[6];
		instructori.append(instructor)



	grupe = []
	cur.execute('select id_grupa from grupe')
	for result in cur:
		grupe.append(result[0])

	tupla = []
	for grupa in grupe:
		query = 'SELECT sali_id_sala FROM grupe WHERE id_grupa=%s' % (grupa)
		cur.execute(query)
		valos = cur.fetchall()
		vals = valos[0][0]
		list = []
		list.append(grupa)
		list.append(vals)
		tupla.append(list)

	sali = []
	cur.execute('select id_sala from sali')
	for result in cur:
		sali.append(result[0])

	cur.close();
	return render_template('instructori.html', instructori=instructori, sali=sali, grupe=tupla)


@app.route('/pianisti')
def _pianisti():
	pianisti=[]
	cur=con.cursor()
	cur.execute('select * from pianisti')
	for result in cur:
		pianist={}
		pianist['id_pianist']=result[0];
		pianist['nume']=result[1];
		pianist['prenume'] = result[2];
		pianist['statut']=result[3];
		pianist['experienta'] = result[4];
		pianist['grupe_id_grupa'] = result[5];
		pianist['grupe_sali_id_sala'] = result[6];
		pianisti.append(pianist)

	grupe = []
	cur.execute('select id_grupa from grupe')
	for result in cur:
		grupe.append(result[0])

	tupla = []
	for grupa in grupe:
		query = 'SELECT sali_id_sala FROM grupe WHERE id_grupa=%s' % (grupa)
		cur.execute(query)
		valos = cur.fetchall()
		vals = valos[0][0]
		list = []
		list.append(grupa)
		list.append(vals)
		tupla.append(list)
	sali = []
	cur.execute('select id_sala from sali')
	for result in cur:
		sali.append(result[0])

	cur.close();
	return render_template('pianisti.html', pianisti=pianisti, grupe=tupla, sali=sali)

@app.route('/spectacole')
def _spectacole():
	spectacole=[]
	cur=con.cursor()
	cur.execute('select * from spectacole')
	for result in cur:
		spectacol={}
		spectacol['id_spectacol']=result[0];
		spectacol['nume_spectacol']=result[1];
		spectacol['capacitate'] = result[2];
		spectacol['data_spectacol']=result[3];
		spectacole.append(spectacol)

	cur.close();
	return render_template('spectacle.html', spectacole=spectacole)

@app.route('/addElev', methods=['POST'])
def ad_elev():
	error = None
	if request.method == 'POST':
		cur = con.cursor()
		values = []

		values.append("'" + request.form['nume'] + "'")
		values.append("'" + request.form['varsta'] + "'")
		values.append("'" + request.form['prenume'] + "'")
		values.append("'" + request.form['statut'] + "'")
		values.append("'" + request.form['grupe_id_grupa'][1] + "'")
		grups="'" +request.form['grupe_id_grupa'][1]+ "'"
		print(grups)
		q='SELECT sali_id_sala from grupe where id_grupa=%s'%(grups)
		cur.execute(q)
		vals=cur.fetchall()
		values.append("'" + str(vals[0][0]) + "'")

		fields = [ 'nume', 'varsta', 'prenume','statut','grupe_id_grupa','grupe_sali_id_sala']
		flag=0
		query1='SELECT COUNT(id_elev) FROM elevi WHERE grupe_id_grupa=%s'% ("'" + request.form['grupe_id_grupa'][1] + "'")
		cur.execute(query1)
		val=cur.fetchall()
		if(val[0][0]<10):
			query = 'INSERT INTO %s (%s) VALUES (%s)' % (
			'elevi',
			', '.join(fields),
			', '.join(values)
			)
			cur.execute(query)
			cur.execute('commit')
			return redirect('/elevi')
		else:
			flash(f"Sunt deja 10 elevi in grupa!","info")
			return redirect('/elevi')



@app.route('/addSpectacol', methods=['POST'])
def ad_spectacol():
	error = None
	if request.method == 'POST':
		cur = con.cursor()
		values = []

		values.append("'" + request.form['nume_spectacol'] + "'")
		values.append("'" + str(10) + "'")
		values.append("'" + request.form['data_spectacol'] + "'")
		fields = [ 'nume_spectacol', 'capacitate', 'data_spectacol']
		query = 'INSERT INTO %s (%s) VALUES (%s)' % (
			'spectacole',
			', '.join(fields),
			', '.join(values)
			)

		cur.execute(query)
		cur.execute('commit')
		return redirect('/spectacole')


@app.route('/addInstructor', methods=['POST'])
def ad_instructor():
	error = None
	if request.method == 'POST':
		cur = con.cursor()
		values = []

		values.append("'" + request.form['nume'] + "'")
		values.append("'" + request.form['prenume'] + "'")
		values.append("'" + request.form['statut'] + "'")
		values.append("'" + request.form['experienta'] + "'")
		values.append("'" + request.form['grupe_id_grupa'][1] + "'")

		grups = "'" + request.form['grupe_id_grupa'][1] + "'"

		q = 'SELECT sali_id_sala from grupe where id_grupa=%s' % (grups)
		cur.execute(q)
		vals = cur.fetchall()
		values.append("'" + str(vals[0][0]) + "'")

		fields = [ 'nume', 'prenume', 'statut', 'experienta', 'grupe_id_grupa', 'grupe_sali_id_sala']
		query = 'INSERT INTO %s (%s) VALUES (%s)' % (
			'instructori',
			', '.join(fields),
			', '.join(values)
			)

		cur.execute(query)
		cur.execute('commit')
		return redirect('/instructori')

@app.route('/addPianist', methods=['POST'])
def ad_pianist():
	error = None
	if request.method == 'POST':
		cur = con.cursor()
		values = []

		values.append("'" + request.form['nume'] + "'")
		values.append("'" + request.form['prenume'] + "'")
		values.append("'" + request.form['statut'] + "'")
		values.append("'" + request.form['experienta'] + "'")
		values.append("'" + request.form['grupe_id_grupa'][1] + "'")
		grups = "'" + request.form['grupe_id_grupa'][1] + "'"
		q = 'SELECT sali_id_sala from grupe where id_grupa=%s' % (grups)
		cur.execute(q)
		vals = cur.fetchall()
		values.append("'" + str(vals[0][0]) + "'")
		fields = [ 'nume', 'prenume', 'statut', 'experienta', 'grupe_id_grupa', 'grupe_sali_id_sala']
		query = 'INSERT INTO %s (%s) VALUES (%s)' % (
			'pianisti',
			', '.join(fields),
			', '.join(values)
			)

		cur.execute(query)
		cur.execute('commit')
		return redirect('/pianisti')


@app.route('/addElevSpectacol', methods=['POST'])
def ad_elevspectacol():
	error = None
	if request.method == 'POST':
		cur = con.cursor()
		values = []

		values.append(request.form['elevi_id_elev'][1])
		grups = "'" + request.form['elevi_id_elev'][1] + "'"
		q = 'SELECT grupe_id_grupa from elevi where id_elev=%s' % (grups)
		cur.execute(q)
		vals = cur.fetchall()
		values.append("'" + str(vals[0][0]) + "'")


		q = 'SELECT grupe_sali_id_sala from elevi where id_elev=%s' % (grups)
		cur.execute(q)
		vals = cur.fetchall()
		values.append("'" + str(vals[0][0]) + "'")


		values.append("'" + request.form['spectacole_id_spectacol'] + "'")

		fields = [ 'elevi_id_elev', 'elevi_id_grupa', 'elevi_id_sala', 'spectacole_id_spectacol']
		query = 'INSERT INTO %s (%s) VALUES (%s)' % (
			'elevi_spectacol',
			', '.join(fields),
			', '.join(values)
			)

		cur.execute(query)
		cur.execute('commit')
		return redirect('/elevi_spect')


@app.route('/delElev', methods=['POST'])
def del_elev():
	id = "'"+request.form['id_elev']+"'"
	cur = con.cursor()
	cur.execute('delete from elevi where id_elev=' + id)
	cur.execute('commit')
	return redirect('/elevi')


@app.route('/delInstructor', methods=['POST'])
def del_instructor():
	id = "'"+request.form['id_instructor']+"'"
	cur = con.cursor()
	cur.execute('delete from instructori where id_instructor=' + id)
	cur.execute('commit')
	return redirect('/instructori')


@app.route('/delPianist', methods=['POST'])
def del_pianist():
	id = "'"+request.form['id_pianist']+"'"
	cur = con.cursor()
	cur.execute('delete from pianisti where id_pianist=' + id)
	cur.execute('commit')
	return redirect('/pianisti')


@app.route('/getElev', methods=['POST'])
def get_elev():
	id = request.form['id_elev']
	cur = con.cursor()
	cur.execute('select * from elevi where id_elev=' + id)

	ids = cur.fetchone()
	id_elev = ids[0]
	statut = ids[1]
	nume = ids[2]
	prenume = ids[3]
	varsta = ids[4]
	grupe_id_grupa = ids[5]
	grupe_sali_id_sala = ids[6]

	grupe = []
	cur.execute('select id_grupa from grupe')
	for result in cur:
		grupe.append(result[0])
	sali = []
	cur.execute('select id_sala from sali')
	for result in cur:
		sali.append(result[0])

	cur.close()
	return render_template('editElevi.html', id_elev=id_elev, statut=statut, nume=nume,prenume=prenume, varsta=varsta, grupe_id_grupa=grupe_id_grupa, grupe_sali_id_sala=grupe_sali_id_sala, grupe=grupe, sali=sali)


@app.route('/editElev', methods=['POST'])
def edit_elev():
	els=0
	cur = con.cursor()

	statut = "'" + request.form['statut'] + "'"
	nume = "'" + request.form['nume'] + "'"
	cur.execute('select id_elev from elevi where nume=' + nume)
	for result in cur:
		els = result[0]
	cur.close()

	prenume= "'" + request.form['prenume'] + "'"
	statut = "'" + request.form['statut']+ "'"
	varsta= request.form['varsta']
	grupe_id_grupa=request.form['grupe_id_grupa']
	grupe_sali_id_sala=request.form['grupe_sali_id_sala']

	cur = con.cursor()
	query = "UPDATE elevi SET statut=%s, nume=%s, prenume=%s, varsta=%s, grupe_id_grupa=%s, grupe_sali_id_sala=%s  where id_elev=%s" % (
	statut, nume, prenume, varsta, grupe_id_grupa, grupe_sali_id_sala, els)
	cur.execute(query)

	return redirect('/elevi')



@app.route('/getInstructor', methods=['POST'])
def get_instructor():
	id = request.form['id_instructor']
	cur = con.cursor()
	cur.execute('select * from instructori where id_instructor=' + id)

	ids = cur.fetchone()
	id_instructor = ids[0]
	nume = ids[1]
	prenume = ids[2]
	statut = ids[3]
	experienta = ids[4]
	grupe_id_grupa = ids[5]
	grupe_sali_id_sala = ids[6]

	grupe = []
	cur.execute('select id_grupa from grupe')
	for result in cur:
		grupe.append(result[0])
	sali = []
	cur.execute('select id_sala from sali')
	for result in cur:
		sali.append(result[0])

	cur.close()
	return render_template('editInstructori.html', id_instructor=id_instructor, statut=statut, nume=nume,prenume=prenume, experienta=experienta, grupe_id_grupa=grupe_id_grupa, grupe_sali_id_sala=grupe_sali_id_sala, grupe=grupe, sali=sali)


@app.route('/editInstructor', methods=['POST'])
def edit_instructor():
	els=0
	cur = con.cursor()


	nume = "'" + request.form['nume'] + "'"
	cur.execute('select id_instructor from instructori where nume=' + nume)
	for result in cur:
		els = result[0]
	cur.close()

	prenume= "'" + request.form['prenume'] + "'"
	statut = "'" + request.form['statut'] + "'"
	experienta= request.form['experienta']
	grupe_id_grupa=request.form['grupe_id_grupa']
	grupe_sali_id_sala=request.form['grupe_sali_id_sala']

	cur = con.cursor()
	query = "UPDATE instructori SET nume=%s, prenume=%s, statut=%s, experienta=%s, grupe_id_grupa=%s, grupe_sali_id_sala=%s  where id_instructor=%s" % (
	 nume, prenume,statut, experienta, grupe_id_grupa, grupe_sali_id_sala, els)
	cur.execute(query)

	return redirect('/instructori')


@app.route('/getPianist', methods=['POST'])
def get_pianist():
	id = request.form['id_pianist']
	cur = con.cursor()
	cur.execute('select * from pianisti where id_pianist=' + id)

	ids = cur.fetchone()
	id_pianist = ids[0]
	nume = ids[1]
	prenume = ids[2]
	statut = ids[3]
	experienta = ids[4]
	grupe_id_grupa = ids[5]
	grupe_sali_id_sala = ids[6]

	grupe = []
	cur.execute('select id_grupa from grupe')
	for result in cur:
		grupe.append(result[0])
	sali = []
	cur.execute('select id_sala from sali')
	for result in cur:
		sali.append(result[0])

	cur.close()
	return render_template('editPianisti.html', id_pianist=id_pianist, statut=statut, nume=nume,prenume=prenume, experienta=experienta, grupe_id_grupa=grupe_id_grupa, grupe_sali_id_sala=grupe_sali_id_sala, grupe=grupe, sali=sali)


@app.route('/editPianist', methods=['POST'])
def edit_pianist():
	els=0
	cur = con.cursor()


	nume = "'" + request.form['nume'] + "'"
	cur.execute('select id_pianist from pianisti where nume=' + nume)
	for result in cur:
		els = result[0]
	cur.close()

	prenume= "'" + request.form['prenume'] + "'"
	statut = "'" + request.form['statut'] + "'"
	experienta= request.form['experienta']
	grupe_id_grupa=request.form['grupe_id_grupa']
	grupe_sali_id_sala=request.form['grupe_sali_id_sala']

	cur = con.cursor()
	query = "UPDATE pianisti SET nume=%s, prenume=%s, statut=%s, experienta=%s, grupe_id_grupa=%s, grupe_sali_id_sala=%s  where id_pianist=%s" % (
	 nume, prenume,statut, experienta, grupe_id_grupa, grupe_sali_id_sala, els)
	cur.execute(query)

	return redirect('/pianisti')


@app.route('/avansareElev', methods=['POST'])
def avans_elev():
	id = request.form['id_elev']
	cur = con.cursor()
	cur.execute('select * from elevi where id_elev=' + id)
	ids = cur.fetchone()

	id_elev=ids[0]
	statut=ids[1]
	nume=ids[2]
	prenume=ids[3]
	varsta=ids[4]
	grupe_sali_id_sala=ids[5]
	grupe_id_grupa=ids[6]


	cur = con.cursor()
	query1='SELECT COUNT(Elevi_id_elev) FROM elevi_spectacol WHERE Elevi_id_elev=%s'%("'"+request.form['id_elev']+"'")
	cur.execute(query1)
	val = cur.fetchall()
	count=val[0][0]

	cur.execute('savepoint f')

	if(count>=5):
		if(statut=='incepator'):

			# query2='UPDATE elevi SET statut=%s WHERE id_elev=%s'%('mediu',id_elev)
			# cur.execute(query2)
			# query3='UPDATE elevi SET grupe_id_grupa= %s '
			query4='DELETE FROM elevi_spectacol WHERE elevi_id_elev=%s'%(id_elev)
			cur.execute(query4)
			cur.execute('savepoint f1')
			cur.execute('commit')


			query5='DELETE FROM elevi WHERE id_elev=%s'%(id_elev)
			cur.execute(query5)
			cur.execute('savepoint f2')
			cur.execute('commit')

			query9 = 'SELECT COUNT(id_elev) FROM elevi WHERE grupe_id_grupa=3'
			cur.execute(query9)
			valo = cur.fetchall()

			query10 = 'SELECT COUNT(id_elev) FROM elevi WHERE grupe_id_grupa=4'
			cur.execute(query10)
			valos = cur.fetchall()
			if (valo[0][0] < 10):
				query6='SELECT sali_id_sala FROM GRUPE WHERE id_grupa=3'
				cur.execute(query6)
				v=cur.fetchall()
				nr=v[0][0]


				values = []

				values.append("'"+str('mediu')+"'")
				values.append("'"+str(nume)+"'")
				values.append("'"+str(prenume)+"'")
				values.append("'"+str(varsta)+"'")
				values.append("'"+str(3)+"'")
				values.append("'"+str(nr)+"'")
				fields = ['statut', 'nume', 'prenume', 'varsta','grupe_id_grupa','grupe_sali_id_sala']
				query = 'INSERT INTO %s (%s) VALUES (%s)' % (
					'elevi',
					', '.join(fields),
					', '.join(values))
				cur.execute(query)
				cur.execute('savepoint f3')
				cur.execute('commit')
			elif(valos[0][0] < 10):
				query12 = 'SELECT sali_id_sala FROM GRUPE WHERE id_grupa=4'
				cur.execute(query12)
				vw = cur.fetchall()
				nr2 = vw[0][0]


				values = []

				values.append("'" + str('mediu') + "'")
				values.append("'" + str(nume) + "'")
				values.append("'" + str(prenume) + "'")
				values.append("'" + str(varsta) + "'")
				values.append("'" + str(4) + "'")
				values.append("'" + str(nr2) + "'")
				fields = ['statut', 'nume', 'prenume', 'varsta', 'grupe_id_grupa', 'grupe_sali_id_sala']
				query = 'INSERT INTO %s (%s) VALUES (%s)' % (
					'elevi',
					', '.join(fields),
					', '.join(values))
				cur.execute(query)
				cur.execute('savepoint f4')
				cur.execute('commit')
			else:
				cur.execute('rollback to savepoint f')

		if (statut == 'mediu'):

			# query2='UPDATE elevi SET statut=%s WHERE id_elev=%s'%('mediu',id_elev)
			# cur.execute(query2)
			# query3='UPDATE elevi SET grupe_id_grupa= %s '
			query4 = 'DELETE FROM elevi_spectacol WHERE elevi_id_elev=%s' % (id_elev)
			cur.execute(query4)
			cur.execute('savepoint f5')
			cur.execute('commit')

			query5 = 'DELETE FROM elevi WHERE id_elev=%s' % (id_elev)
			cur.execute(query5)
			cur.execute('savepoint f6')
			cur.execute('commit')

			query9 = 'SELECT COUNT(id_elev) FROM elevi WHERE grupe_id_grupa=5'
			cur.execute(query9)
			valo = cur.fetchall()

			query10 = 'SELECT COUNT(id_elev) FROM elevi WHERE grupe_id_grupa=6'
			cur.execute(query10)
			valos = cur.fetchall()
			if (valo[0][0] < 10):
				query6 = 'SELECT sali_id_sala FROM GRUPE WHERE id_grupa=5'
				cur.execute(query6)
				v = cur.fetchall()
				nr = v[0][0]

				values = []

				values.append("'" + str('avansat') + "'")
				values.append("'" + str(nume) + "'")
				values.append("'" + str(prenume) + "'")
				values.append("'" + str(varsta) + "'")
				values.append("'" + str(5) + "'")
				values.append("'" + str(nr) + "'")
				fields = ['statut', 'nume', 'prenume', 'varsta', 'grupe_id_grupa', 'grupe_sali_id_sala']
				query = 'INSERT INTO %s (%s) VALUES (%s)' % (
					'elevi',
					', '.join(fields),
					', '.join(values))
				cur.execute(query)
				cur.execute('savepoint f7')
				cur.execute('commit')
			elif (valos[0][0] < 10):
				query12 = 'SELECT sali_id_sala FROM GRUPE WHERE id_grupa=6'
				cur.execute(query12)
				vw = cur.fetchall()
				nr2 = vw[0][0]

				values = []

				values.append("'" + str('avansat') + "'")
				values.append("'" + str(nume) + "'")
				values.append("'" + str(prenume) + "'")
				values.append("'" + str(varsta) + "'")
				values.append("'" + str(6) + "'")
				values.append("'" + str(nr2) + "'")
				fields = ['statut', 'nume', 'prenume', 'varsta', 'grupe_id_grupa', 'grupe_sali_id_sala']
				query = 'INSERT INTO %s (%s) VALUES (%s)' % (
					'elevi',
					', '.join(fields),
					', '.join(values))
				cur.execute(query)
				cur.execute('savepoint f8')
				cur.execute('commit')
			else:
				cur.execute('rollback to savepoint f')

		if (statut == 'avansat'):
			# query2='UPDATE elevi SET statut=%s WHERE id_elev=%s'%('mediu',id_elev)
			# cur.execute(query2)
			# query3='UPDATE elevi SET grupe_id_grupa= %s '
			cur.execute('savepoint g')
			query4 = 'DELETE FROM elevi_spectacol WHERE elevi_id_elev=%s' % (id_elev)
			cur.execute(query4)
			cur.execute('savepoint f9')
			cur.execute('commit')

			query5 = 'DELETE FROM elevi WHERE id_elev=%s' % (id_elev)
			cur.execute(query5)
			cur.execute('savepoint f10')
			cur.execute('commit')

			query9 = 'SELECT COUNT(id_elev) FROM elevi WHERE grupe_id_grupa=7'
			cur.execute(query9)
			valo = cur.fetchall()

			query10 = 'SELECT COUNT(id_elev) FROM elevi WHERE grupe_id_grupa=8'
			cur.execute(query10)
			valos = cur.fetchall()
			if (valo[0][0] < 10):
				query6 = 'SELECT sali_id_sala FROM GRUPE WHERE id_grupa=7'
				cur.execute(query6)
				v = cur.fetchall()
				nr = v[0][0]

				values = []

				values.append("'" + str('avansat') + "'")
				values.append("'" + str(nume) + "'")
				values.append("'" + str(prenume) + "'")
				values.append("'" + str(varsta) + "'")
				values.append("'" + str(7) + "'")
				values.append("'" + str(nr) + "'")
				fields = ['statut', 'nume', 'prenume', 'varsta', 'grupe_id_grupa', 'grupe_sali_id_sala']
				query = 'INSERT INTO %s (%s) VALUES (%s)' % (
					'elevi',
					', '.join(fields),
					', '.join(values))
				cur.execute(query)
				cur.execute('savepoint f11')
				cur.execute('commit')
			elif (valos[0][0] < 10):
				query12 = 'SELECT sali_id_sala FROM GRUPE WHERE id_grupa=8'
				cur.execute(query12)
				vw = cur.fetchall()
				nr2 = vw[0][0]

				values = []

				values.append("'" + str('avansat') + "'")
				values.append("'" + str(nume) + "'")
				values.append("'" + str(prenume) + "'")
				values.append("'" + str(varsta) + "'")
				values.append("'" + str(8) + "'")
				values.append("'" + str(nr2) + "'")
				fields = ['statut', 'nume', 'prenume', 'varsta', 'grupe_id_grupa', 'grupe_sali_id_sala']
				query = 'INSERT INTO %s (%s) VALUES (%s)' % (
					'elevi',
					', '.join(fields),
					', '.join(values))
				cur.execute(query)
				cur.execute('savepoint f12')
				cur.execute('commit')
			else:
				cur.execute('rollback to savepoint g')
		if(statut=='profesionist'):
			cur.execute('rollback to savepoint f')


	return redirect('/elevi')





if __name__ == '__main__':
	app.run(debug=True)
	con.close()