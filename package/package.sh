mkdir akalabeth
cp -f ../*.py akalabeth/
cp -f ../*.pyxres akalabeth/
cp -f ../AKA* akalabeth/
pyxel package akalabeth akalabeth.py
rm -rf akalabeth