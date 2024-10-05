import subprocess
import os


def levantar_docker_compose():
    try:
        # Cambiar al directorio donde está el archivo docker-compose.yaml
        os.chdir(r"D:\0002- Proyectos\API WHATSAPP\evolution-api-main\Docker")

        # Comando para levantar docker-compose
        subprocess.run(["docker-compose", "up", "--build"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al levantar Docker Compose: {e}")
    except FileNotFoundError:
        print("Docker o Docker Compose no está instalado o no está en la ruta del sistema.")


if __name__ == "__main__":
    levantar_docker_compose()
