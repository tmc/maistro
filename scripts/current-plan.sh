cd output/
cd $(ls |tail -n1)/
cat $(ls *step*yaml |tail -n1) | yq -C .
