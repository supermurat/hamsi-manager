#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Core import Universals, Variables

def getUtf8Data(_key):
    unicodeData = ""
    try:
        if _key=="replacementChars":
            unicodeData = {"Ý" : "İ", "ý" : "ı", "þ" : "ş", "Ð" : "ğ", "Þ" : "Ş", "Ã" : "Ü", "Ã¼" : "ü", "Ä°Å" : "İ", "Ã" : "ç", "Ä±" : "ı","Å" : "ş", "Ã§" : "ç", "Ã¶" : "ö", "Ä" : "ğ", "Ä°" : "İ", "Ã" : "Ö", "Ã" : "Ö", "Â³" : "ü", "Ä" : "ğ", "Å" : "Ş","Ä" : "Ğ","Å" : "ş", "Ã§" : "ç", "" : "ö" , "" : "Ö" ,"Ã" : "Ö", "" : "İ" , "Â¦" : "ı" , "" : "I" ,"ÃÂ°" : "İ","Ã½" : "ı","Ã" : "i","ï¿½" : "İ", "" : "ü" , "" : "Ü" , "Â³" : "Ü", "" : "Ç" , "" : "ç" , "§" : "ğ" ,"¦" : "Ğ","ä" : "ğ","Ä" : "Ğ","Ä" : "ğ","Ã°" : "ğ","ã" : "ğ","Ã" : "Ğ","ð" : "ğ", "" : "Ş" ,"Ã" : "Ş" , "" : "ş" ,"å" : "ş","ã" : "ş","å" : "ş","Ã¾" : "ş","ã¾" : "ş", "_" : " ","ã" : "","Ã" : "","å" : "","Å" : ""}
        elif _key=="upright":
            return "│"
        elif _key=="upright+right":
            return "├"
        elif _key=="up+right":
            return "└"
        elif _key=="little+I":
            return "ı"
        elif _key=="":
            return ""
    except Exception as err:
        Universals.printForDevelopers(str(err))
    return unicodeData



