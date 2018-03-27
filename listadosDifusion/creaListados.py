# coding: utf-8

import csv
import pandas as pd
import json

argentina={
'buenosaires':{'name': 'Buenos Aires','coord':'-34.60551942876607,-58.45550537109375','xoeste' : -63,'ynorte': -33 ,'xeste': -56,'ysur': -41,'words':['caba','bs','as','buenos','aires','ba','pba','plata','blanca','tuyu','necochea','batan','otamendi','chapadmalal','azul','bayas','demarchi','triunfo','arenza','roberts','pasteur','algarrobos','banderalo','bunge','charlone','germania','alem','carabelas','alfonzo','ocampo','acevedo','millan','tala','conesa','castro','ramallo','olivera','torres','solis','riestra','pedrenales','cachari','fortabat','mansilla','atalaya','indio','pipinas','copelo','sol','orlando','gesell','tandil','junin','chascomus','olavarria','puan','pergamino','pedro','quilmes','lanus','avellaneda','mercedes','lujan','chivilcoy','zarate','arroyos','zamora','trenque','lauquen','pehuajo','moron','tigre','paz','pilar','olivos','isidro','ituzaingo','caseros','stroeder','villalonga','pradere','luro','ascasubi','buratovich','couste','cerri','darragueira','rivera','lima','bernardo','patagones','medanos','villegas','ayacucho','carhue','lincol','pringles','bolivar','guamini','loberia','rauch','tornquist','tapalque','balcarce','tejedor',' daireaux','pila','flores','vidal','madariaga','guido','cayetano','saladillo','maipu','pinto','casares','chacabuco','bahia','blanca','bragado','toldos','chivilcoy','castelli','rojas','monte','ameghino','pellegrini','magdalena','lobos','henderson','navarro','salto','veronica','vedia','miramar','arenales','baradero','conesa','lomas','zamora','areco','lezama','brandsen','mercedes','campana','salliquelo','suipacha','escobar','ezeiza','berazategui','moreno','berisso','merlo','adrogue','guernica','ensenada','polvorines','hurlingham','agronomía','almagro','balvanera','barracas','belgrano','boedo','caballito','chacarita','coghlan','colegiales','constitución','flores','floresta','boca','paternal','liniers','mataderos','castro','montserrat','pompeya','nuñez','palermo','chacabuco','chas', 'patricios','madero','recoleta','retiro','saavedra','cristobal','nicolas','telmo','versalles','crespo','devoto','mitre','lugano','luro','ortuzar','pueyrredon','real','riachuelo','rita','soldati','urquiza','parque','sarsfield']},
'cordoba':{'name': 'Cordoba','coord':'-31.42008329999999,-64.18877609999998','xoeste' : -65,'ynorte': -29 ,'xeste': -61,'ysur': -34, 'words':['cor','cordoba','cba','carlos','paz','capilla','belgrano','oliva','marcos','juarez','carlota','renanco','laboulaye','mackenna','joyita','giardino','colorado','fransisco','huidobro','bell','ville','tulumba','carlota','laboulaye','olivia','dean','funes','minas','gracia','brochero','chañar','salsacate','totoral','cosquin']},
'santafe':{'name': 'Santa Fe','coord':'-31.6106578,-60.697294','xoeste' : -61,'ynorte': -28 ,'xeste': -59,'ysur': -34,'words':['sf','sta', 'fe','santa','rosario','tostado','reconquista','vera','venado','tuerto','trebol','rafaela','rufino','gregorio','carmen','maggiolo','cafferata','chañar','ladeado','godeken','quirquinchos','firmat','villada','bombal','bigand','mugueta','teresa','galvez','perez','roldan','carcaraña','armstrong','baigorria','fighiera','seco','tome','rincon','recreo','paiva','sunchales','ceres','obligado','iriondo','helvecia','casilda','castellanos','colonias','coronda','melincue']},
'mendoza':{'name': 'Mendoza','coord':'-32.8894587,-68.84583859999998','xoeste' : -70,'ynorte': -32 ,'xeste': -66,'ysur': -37,'words':['mza','mendoza','rafael','heras','inca','atuel','iselin','goudge','prats','rosas','caida','lorca','martin','consulta','tupungato','vegas','jocoli','desaguadero','malargue','cuyo','tunuyan','guaymallen']},
'tucuman':{'name': 'Tucuman','coord':'-26.8082848,-65.21759029999998','xoeste' : -66,'ynorte': -26 ,'xeste': -64,'ysur': -27,'words':['tucu','tucuman','miguel','chulca','colalao','concepcion','tafi','ancajuli','taco','ralos','ranchillo','amaicha','nio','mollar','piedrabuena','lules','simoca','aguilares','yunca','suma','cocha','burruyacu','trancas','chicligasta','simoca','graneros','lules','famailla']},
'lapampa':{'name': 'La Pampa','coord':'-36.6147573,-64.2839209','xoeste' : -68,'ynorte': -35 ,'xeste': -63,'ysur': -39,'words':['pampa','lp','rosa','pico','puelches','bernasconi','acha','victorica','castex','catriel','puelen','curaco','utracan','calel','lihuel','limay','mahuida','loventue','caleu','chical','chalileo','hucal','toay','conhelo','rancul','parera','atreuco','macachin','guatrache','chapaleufu','quemu','maraco','catrilo','realico','trenel']},
'sanluis':{'name': 'San Luis','coord':'-33.3017267,-66.33775220000001','xoeste' : -67,'ynorte': -31 ,'xeste': -64,'ysur': -35,'words':['luis','sl','trapiche','merlo','mapa','recuerdo','estrella','loyola','union','arizona','maroma','reynolds','balde','algarrobo','beazley','fraga','talita','toma','tilisarao','zanjitas','dupuy','pedernera','concaran','conlara']},
'corrientes':{'name': 'Corrientes','coord':'-27.4692131,-58.83063490000001','xoeste' : -59,'ynorte': -27 ,'xeste': -55,'ysur': -30,'words':['corrientes','cor','goya','lorenzo','curuzu','cuatia','chavarria','cazadores','ita','cora','empedrado','perugorria','tabay','saladas','virasoro','pujol','perugorria','lavalle','tabay','olivari','tome','esquina','palmar','itati','astrada','cosme','mburucuya']},
'entrerios':{'name': 'Entre Rios','coord':'-31.77411146499047,-60.49548625946045','xoeste' : -60,'ynorte': -30 ,'xeste': -57,'ysur': -33,'words':['entre','rios','er','parana','federal','paz','colon','gualeguay','gualeguaychu','feliciano','nogoya','villaguay','concepcion','diamante','tala','gustuvo','gualeguay','victoria','elisa','cimarron','aranqueren','crespo','aranguren','chajari','elena','ibicuy','concordia','feliciano','diamante','tala']},
'misiones':{'name': 'Misiones','coord':'-27.4269255,-55.94670759999997','xoeste' : -56,'ynorte': -25 ,'xeste': -53,'ysur': -27,'words':['mis','misiones','guarani','posadas','obera','otaño','eldorado','dorado','apostoles','america','azara','rico','cainguas','apostoles','iguazu','magdalena','garupa','aristobulo','caraguatay','garuhape','andresito','wanda','magdalena','pinares','piray','taruma']},
'chaco':{'name': 'Chaco','coord':'-27.4518622,-58.985554699999966','xoeste' : -63,'ynorte': -24 ,'xeste': -58,'ysur': -27,'words':['cho','chaco','rcia','resistencia','barranqueras','charata','roque', 'saenz','pozo','muerto','angela','roque','isletas','vilelas','fontana','barranqueras','wichi','sauzal','sauzalito','bermejito','palamas','benitez','solari','frentones','avia','terai','gancedo','basail','cabral','ohiggins','quitilipi','donovan']},
'formosa':{'name': 'Formosa','coord':'-26.1857768,-58.175566900000035','xoeste' : -62,'ynorte': -22 ,'xeste': -57,'ysur': -26,'words':['fsa','formosa','cañitas','junta','escondido','rivadavia','matacos','patiño','pirañe','pilcomayo','laishi','juarez','fontana','clorinda','espinillo','ramon','lista','pilagas']},
'salta':{'name': 'Salta','coord':'-24.7821269,-65.42319759999998','xoeste' : -68,'ynorte': -22 ,'xeste': -62,'ysur': -26,'words':['salta','sal','tartagal','cafayate','metan','rivadavia','joaquin','gonzalez','ramon','oran','embarcacion','iruya','poma','lerma','molinos','cachi','cerrillos','chicoana','viña','anta','oran','poma','molinos','guachipas','frontera','caldera']},
'santiago':{'name': 'Santiago del Estero','coord':'-27.7833574,-64.26416699999999','xoeste' : -65,'ynorte': -27 ,'xeste': -61,'ysur': -30,'words':['santiago','estero','sgo','est','se','bandera','esperanza','quemado','bandera','armonia','quimili','hondo','frias','choya','taboada','salavina','guasayan','atamisqui','hondo','robles','silipica']},
'jujuy':{'name': 'Jujuy','coord':'-24.1843397,-65.30217700000003','xoeste' : -67,'ynorte': -21 ,'xeste': -64,'ysur': -24,'words':['jujuy','juj','salvador','tilcara','humauaca','perico','calilegua','purmamarca','casabindo','catalina','rinconada','susques','tumbaya','poma','iruya','yavi','cochinoca','palpala']},
'larioja':{'name': 'La Rioja','coord':'-29.4134538,-66.85645790000001','xoeste' : -28,'ynorte': -27 ,'xeste': -29,'ysur': -31,'words':['rioja','lr','ulapes','chilecito','chamical','olta','milagro','sanagasta','union','logrono','chepes','catunia','desidero','toma','malazan','miranda','famatina','mesada','anillaco','guandacol','vinchina','peñazola','tama','quiroga','aminga']},
'catamarca':{'name': 'Catamarca','coord':'-28.4715877,-65.78772090000001','xoeste' : -68,'ynorte': -25 ,'xeste': -64,'ysur': -29,'words':['catamarca','cat','fernando','fiambala','belen','tinogasta','recreo','peladas','antofagasta','antofalla','rodeo','capayan','arauco','poman','andalgala','poman','arauco','ancasti','saujil','huillapima','ovanta','merced']},
'sanjuan':{'name': 'San Juan','coord':'-31.5351074,-68.53859410000001','xoeste' : -70,'ynorte': -28 ,'xeste': -66,'ysur': -32,'words':['juan','sn','sj','caucete','media','agua','tamberias','corral','bermejo','jachal','tucunuco','krause','chimbas','calingasta','jachal','caucete','ullum','zonda','angaco','albardon','pocito']},
'neuquen':{'name': 'Neuquen','coord':'-38.9516784,-68.05918880000002','xoeste' : -37,'ynorte': -70 ,'xeste': -38,'ysur': -71,'words':['neuquen','aguila','martin','bariloche','neu','nn','zapala','centenario','cutral','añelo','ranquil','collon','ñorquin','lajas','picunches','loncopue','huecu','zapala','lacar','alumine','picun','leufu','malal','huiliches','andes','angostura','aguila','plottier','cutral','huincul','sauces','añelo','ranquil','pehuenches','confluencia']},
'rionegro':{'name': 'Rio Negro','coord':'-40.8261434,-63.02663389999998','xoeste' : -70,'ynorte': -38 ,'xeste': -62,'ysur': -41,'words':['rio','negro','rn','viedma','bariloche','roca','menucos','maquinchao','choel','lamarque','mallin','mascardi','coihues','dina','huapi','llanquin','comallo','cañadon','limay','mencue','naupa','huen','colan','conhue','jacobacci','mamuel','choique','pilquiniyeu','cain','prahuaniyeu','yaminue','treneta','cona','niyeu','berros','paileman','cecilio','grutas','cipolletti','allen','maquinchao','cuy','valcheta','pichi','mauida','pilcaniyeu','ñorquinco']},
'chubut':{'name': 'Chubut','coord':'-43.2934246,-65.11148179999998','xoeste' : -72,'ynorte': -42 ,'xeste': -63,'ysur': -45,'words':['chubut','cht','rawson','trelew','esquel','madryn','comodoro','rivadavia','piramides','valdez','delgada','camarones','rawson','beleiro','rada','tilly','astra','garayalde','apleg','viglioni','corcovado','carrenleufu','cipreses','trevelin','futalaufquen','cholila','epuyen','bolson','puelo','maiten','cushamen','fofo','cahuel','blancuntre','gan','escorial','altares','mirasol','dolavon','garayalde','diadema','senguer','telsen','gastre','leleque','camarones','cushamen','tecka','languiñeo','tehuelches','biedma','gaiman','futaleufu']},
'santacruz':{'name': 'Santa Cruz','coord':'-51.6352821,-69.2474353','xoeste' : -73,'ynorte': -45 ,'xeste': -65,'ysur': -52,'words':['cruz','sc','sta','gallegos','chalten','calafate','deseado','gregores','truncado','caleta','jaramillo','rospentek','dufour','turbio','caracoles','koluel','kaike','cañadon','tellier','julian','corpen','aike','magallanes']},
'tierradelfuego':{'name': 'Tierra del Fuego','coord':'-54.8053998,-68.32420609999997','xoeste' : -68,'ynorte': -52 ,'xeste': -65,'ysur': -54,'words':['tf','ta','fgo','tierra','fuego','despedida','tolhuin','ushuaia','cullen','escondida']}}

def load_dicts(pais):
    words = {}
    cant_words = {}
    dicc_usuarios = {}
    for prov in pais:
        cant_words[prov] = 0
    for prov in pais:
        print(prov)
        with open(path + prov + '_dict.json') as fi:
            words[prov] = json.load(fi)
        cant_words[prov] = cant_palabras(words[prov])
        with open(path + prov + '_users_dict.json') as fi:
            dicc_usuarios[prov] = json.load(fi)

    return (words, cant_words, dicc_usuarios)

def cant_palabras(dicc):
    return sum(dicc.values())

path = '../../Desktop/datosTesis/train/ultimosJson/train_'

wcd = load_dicts(argentina)
lugares = argentina

words = wcd[0]
cant_words = wcd[1]
dicc_usuarios = wcd[2]

cantPorLugar = {lugar: sum(words[lugar].values()) for lugar in lugares}

users_cant = {}
for lugar in lugares:
    for pal, lista in dicc_usuarios[lugar].items():
        # print lugar,pal,lista
        if lugar not in users_cant:
            users_cant[lugar] = {}
            users_cant[lugar][pal] = len(lista)
        else:
            users_cant[lugar][pal] = len(lista)
df = pd.DataFrame(words)
df1 = pd.DataFrame(users_cant)
print(df.shape)
print(df1.shape)
df = df.fillna(0)
df1 = df1.fillna(0)
df.columns = [str(col) + 'Palabras' for col in df.columns]
df1.columns = [str(col) + 'Personas' for col in df.columns]
df1['cantUsuariosTotal'] = df1.sum(axis=1)
df['cantPalabra'] = df.sum(axis=1)

result = pd.concat([df, df1], axis=1)

print("Cantidad de palabras: {}".format(result.cantPalabra.sum()))
result.to_csv('cantidadesTotales.csv',encoding='utf-8')

result.sort_values(by='cantPalabra',ascending=False,inplace=True)
result.to_csv('cantidadesTotalesOrdenada.csv',encoding='utf-8')
result.loc[result.cantPalabra > 40].to_csv('cantidadesDatasetFiltrado.csv',encoding='utf-8')
