from django.conf import settings
import os


def get_upload_path(instance, filename):
	try:
		try:
			index = filename.index('.')
			_filename = filename[index:]
		except:
			_filename = ''

		__filename = repr(instance).split(':')[0].strip('<')+'_'+str(instance.id)+_filename
	except:
		ruta = os.path.join(instance.REPOSITORIO, "%s" % filename)
	else:
		ruta = os.path.join(instance.REPOSITORIO, "%s" % __filename)

	return ruta

def guarda_archivo(archivo, destino):
	d = open(os.path.join(destino, archivo.name.split('/')[-1]), 'wb+')
	for chunk in archivo.chunks():
			d.write(chunk)
	d.close()    
	return d.name

def move_document(archivo, objInstance):
	try:
		destino = objInstance.HISTORICO
	except Exception, e:
		return None

	if os.path.isfile(archivo.path) and destino != '':
		_archivo = guarda_archivo(archivo, destino)
		return _archivo
	else:
		return None