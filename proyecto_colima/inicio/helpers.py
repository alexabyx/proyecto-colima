import os

def get_upload_path(instance, filename):
	ruta = os.path.join(instance.REPOSITORIO, filename)
	return ruta