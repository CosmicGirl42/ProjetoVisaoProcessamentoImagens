# <CLASS>-<ID>-<BACKGROUND>-<HORA>-<LUGAR>-<VERSÂO>

# LIBS
# std libs

import glob
import os
import sys

# external libs
from matplotlib import pyplot
import cv2


def get_files(folder: str):
    """
    Get all files in the `db` folder and then returns the filename (metadata) and the openned images and the size in bytes.

    Parameters:
    folder: str
    """
    files = glob.glob(f"{folder}/*")

    zipped_filename_images_size = []

    for file in files:
        zipped_filename_images_size.append(
            (
                os.path.basename(file).split(".")[0],
                cv2.imread(file, cv2.IMREAD_GRAYSCALE),
                os.path.getsize(file),
            )
        )

    return zipped_filename_images_size


def add_to_env(env, filename: str, image, size: int):
    """
    Insert a image to the `env`

    Parameters:
    env: Dict[str, Dict[str, List[Dict[str, str|Any]]]]
    filename: str
    image: Image
    size: int
    """
    # Really, who thought exceptions was a good idea? I want strongly typed errors
    # I want to know at the type level what error can occur
    # Also, the syntax is ugly 😠
    try:
        clas, i_d, bg, place, time, version = filename.split("-")

        # Ugh, I just wanted the Rust entry API here, it would reduce the following code to a 4 liner code T-T
        if env.get(clas) == None:
            env[clas] = dict()

        if env[clas].get(i_d) == None:
            env[clas][i_d] = list()

        env[clas][i_d].append(
            {
                "background": bg,
                "time": time,
                "place": place,
                "version": version,
                "size": size,
                "image": image,
            }
        )
    except ValueError:
        print(
            f"Failed to add {filename} to the environment: The name of the file is badly formated"
        )
    except:
        print(
            f"Failed to add {filename} to the environment for unknown reasons: {sys.exc_info()[0]}"
        )


def print_info(env):
    """
    Print DB info

    Parameters:
    env: Dict[str, Dict[str, List[Dict[str | Any]]]]
    """
    n_classes = len(env)
    n_images = 0
    db_size = 0
    image_col, image_line = (720, 1280)

    classes_info = []
    for clas, dic in env.items():
        bg = set()
        lumen = set()
        total_samples = 0

        for (i_d, xs) in dic.items():
            for item in xs:
                bg.add(item["background"])
                lumen.add(f"{item['time']}+{item['place']}")
                total_samples += 1
                n_images += 1
                db_size += item["size"]

        classes_info.append(
            f"{clas} | {len(dic)} objetos | {len(bg)} variações de fundo {bg} | {len(lumen)} variações de iluminação {lumen} | 3 repetições | {total_samples} amostras"
        )

    # general
    print(
        f"""===================================

Tabela Global Sumária

Nome do Atributo | Atributo

Número de classes | {n_classes}

Número de imagens | {n_images}

Tamanho da base (bytes) | {db_size / (1024*1024)} MB

Resolução das imagens | {image_line} linhas por {image_col} colunas

=================================

Tabela detalhada por classe
"""
    )

    for i in classes_info:
        print(f"{i}")

    print("=================================")


def plot_mnist(env):
    """
    Plot one image of every class in a mnist like manner.

    Parameters:
    images: List[Image]
    """
    for index, clas in enumerate(env.keys()):
        image = env[clas]["1"][0]["image"]
        pyplot.subplot(2, 5, index + 1)
        pyplot.imshow(image, cmap=pyplot.get_cmap("gray"))

    pyplot.tight_layout()
    pyplot.show()