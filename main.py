from lexical_analysis import LexicalAnalysis 

def main():
    al = LexicalAnalysis()
    while True:
        try:
            token = al.nextToken()
            if (token == None):
                break
            else:
                print(token)
        except Exception as e:
            print(e)


if (__name__ == '__main__'):
    main()