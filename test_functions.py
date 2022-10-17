from functions import *


# Test des fonctions avec > pytest


def test_rechercheRegEx():
    assert rechercheRegEx(["123456", "1234", "12345X"], [
                          "1234", "123456", "123456"]) == [True, False, False]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


def test_rechercheRegExPartiellePareil():
    assert rechercheRegExPartielle("12345", "12345") == True


def test_rechercheRegExPartielleCourt1():
    assert rechercheRegExPartielle("123", "12345") == True


def test_rechercheRegExPartielleCourt2():
    assert rechercheRegExPartielle("12345", "123") == True


def test_rechercheRegExPartielleFalse1():
    assert rechercheRegExPartielle("12345", "1234X") == False


def test_rechercheRegExPartielleFalse2():
    assert rechercheRegExPartielle("1234X", "12345") == False


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def test_prepString1():
    assert prepString("(C,H,T)12*+-/") == ".12."


def test_prepString2():
    assert prepString("12345A$%") == "12345A$%"


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Ajouter test findMatch et findMatchPartiels
