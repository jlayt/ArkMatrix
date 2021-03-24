python arkmatrix.py test/bonn.lst
python arkmatrix.py test/cycle.lst
python arkmatrix.py test/reduce.lst
python arkmatrix.py test/stratify.lst
python arkmatrix.py -n name -t site test/stratify.lst
python arkmatrix.py -o graphml test/bonn.lst
python arkmatrix.py -s -o graphml test/bonn.lst
python arkmatrix.py -o gml test/bonn.lst
python arkmatrix.py -s -o gml test/bonn.lst
python arkmatrix.py -o gv test/bonn.lst
python arkmatrix.py -s -o gv test/bonn.lst
python arkmatrix.py -o dot test/bonn.lst
python arkmatrix.py -s -o dot test/bonn.lst
python arkmatrix.py -o tgf test/bonn.lst
python arkmatrix.py -s -o tgf test/bonn.lst
python arkmatrix.py -o gxl test/bonn.lst
python arkmatrix.py -s -o gxl test/bonn.lst
python arkmatrix.py -o csv test/bonn.lst
python arkmatrix.py -s -o csv test/bonn.lst
python arkmatrix.py -r -o graphml test/reduce.lst
python arkmatrix.py -o csv test/csv_simple.csv
python arkmatrix.py test/csv_format.csv
python arkmatrix.py --group test/csv_format.csv
