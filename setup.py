from setuptools import setup, find_packages

setup(
    name="BalizStealerBuilder",
    packages=find_packages(),
    install_requires=[
        "customtkinter",
        "Pillow",
        "requests",
        "psutil",
        "pyperclip",
        "pyautogui",
        "opencv-python",
        "pywin32",
        "pycryptodome",
    ],
    python_requires='>=3.7',
)
