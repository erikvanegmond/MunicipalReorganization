import loadData as ld

# fixBeschrijvingen("testt.txt", 'testt.txt')
# fixBeschrijvingen("beschrijving.txt", 'beschrijving.txt')
# fixBeschrijvingen("beschrijving.txt", 'beschrijving.txt')

gebiedenDict, gebiedenNameDict = ld.loadGebieden()


test =  ld.loadDataListFromTXT("testt.txt", gebiedenNameDict, gebiedenDict)


# To return a new list, use the sorted() built-in function...
newlist = sorted(test, key=lambda x: x.code, reverse=False)


# for t in newlist:
#     t.pprint()