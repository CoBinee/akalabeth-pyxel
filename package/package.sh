mkdir akalabeth
cp -f ../akar.py akalabeth/
cp -f ../*.pyxres akalabeth/
cp -f ../AKA* akalabeth/
pyxel package akalabeth akar.py
rm -rf akalabeth