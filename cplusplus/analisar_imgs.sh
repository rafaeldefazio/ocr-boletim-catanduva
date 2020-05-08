for f in *.jpg
do
	./ocr_boletim $f &
done

wait
