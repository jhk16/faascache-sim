#!/bin/sh

# wsk property set \
#   --apihost 'http://172.17.0.1:3233' \
#   --auth 'babecafe-cafe-babe-cafe-babecafebabe:007zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'

# cd ./load-test
# python3 ./linear_run.py
# cd ..

wsk -i action update py_act_web ./py/json_dumps_loads.zip --web true --kind python:3
wsk -i action invoke --result py_act_web
# curl "http://172.17.0.1:3233/api/v1/web/alftest/py/net"

# wsk action update js_act_1 ./js/hello.js
# wsk action update js_act_2 ./js/two.js
# wsk action update js_act_3 ./js/three.js

# wsk action invoke --result js_act_1 --param name ben
# wsk action invoke --result js_act_1 --param name quad
# wsk action invoke --result js_act_1 --param name ben
# wsk action invoke --result js_act_1 --param name quad

# wsk action invoke --result js_act_2 --param name ben
# wsk action invoke --result js_act_2 --param name kenobi
# wsk action invoke --result js_act_2 --param name ben
# wsk action invoke --result js_act_2 --param name kenobi

# wsk action invoke --result js_act_3 --param name ben
# wsk action invoke --result js_act_3 --param name uncle
# wsk action invoke --result js_act_3 --param name ben
# wsk action invoke --result js_act_3 --param name uncle

# wsk -i action update py_act_hello --memory 400 --kind python:3 ./py/hello.zip
# wsk -i action invoke --result py_act_hello --param name world

# wsk -i action update py_act_cham --memory 512 --kind python:3 ./py/chameleon.zip
# wsk -i action invoke --result py_act_cham --param num_of_rows 10 --param num_of_cols 10

# wsk -i action update py_act_float --memory 512 --kind python:3 ./py/float_operation.zip
# wsk -i action invoke --result py_act_float --param n 20

# wsk -i action update py_act_lin_pack --memory 512 --kind python:3 ./py/lin_pack.zip
# wsk -i action invoke --result py_act_lin_pack --param n 20

# wsk -i action update py_act_pyaes --memory 512 --kind python:3 ./py/pyaes.zip
# wsk -i action invoke --result py_act_pyaes --param length_of_message 200 --param num_of_iterations 200

wsk -i action update py_act_cnn --memory 1024 --kind python:3 ./py/cnn_image_classification.zip
wsk -i action invoke --result py_act_cnn

# wsk -i action update py_act_vid --memory 1024 --kind python:3 ./py/video_processing.zip
# wsk -i action invoke --result py_act_vid

# wsk -i action update py_act_img --memory 1024 --kind python:3 ./py/image_processing.zip
# wsk -i action invoke --result py_act_img

# wsk -i action update py_act_train --memory 1024 --kind python:3 ./py/model_training.zip
# wsk -i action invoke --result py_act_train

# wsk -i action update py_act_gzip --memory 1024 --kind python:3 ./py/gzip_compression.zip
# wsk -i action invoke --result py_act_gzip

# wsk -i action update py_act_dd --memory 1024 --kind python:3 ./py/dd.zip
# wsk -i action invoke --result py_act_dd

# wsk -i action update py_act_net --memory 256 --kind python:3 ./py/json_dumps_loads.zip
# wsk -i action invoke --result py_act_net
