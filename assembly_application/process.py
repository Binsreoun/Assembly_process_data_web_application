import numpy as np
import pandas as pd
import time
from datetime import datetime, timedelta
import joblib
from machine import machine_operate
from SQL import MySQL_query

class process_operate:

    def process_start(amount):
        std = 0.0025  # 표준편차

        ## 초기 셋업 타임 설정
        op10_setup_time = 0
        op20_setup_time = 0
        op30_setup_time = 0
        op40_setup_time = 0
        op50_setup_time = 0
        op60_setup_time = 0

        stop_button = None  # 정지 버튼 True 되면 공정 스탑 하고 정지하거나 리셋


        ##### 전체적인 진행: body 생성 -> op10 실행 -> DB 저장 -> 저장한 데이터 가져오기 -> op10_data 변수 저장 -> 다음 공정 실행


        body_P0 = []  # 공정에 넣을 body 데이터 리스트 틀

        product_key_W1P0 = '-' + 'W1' + 'P' + str(0)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P0.append(product_key_W1P0)

        body_l_P0 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P0 = round(body_l_P0, 5)
        body_P0.append(body_l_P0)

        body_w_P0 = np.random.normal(100, std)
        body_w_P0 = round(body_w_P0, 5)
        body_w_P0.append(body_w_P0)

        body_h_P0 = np.random.normal(50, std)
        body_h_P0 = round(body_h_P0, 5)
        body_P0.append(body_h_P0)

        op10_process_time_P0 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P0 = round(op10_process_time_P0, 5)

        body_P0.append(op10_process_time_P0)
        body_P0.append(datetime.now())  # 첫번째 제품은 현재시간부터 시작한다고 가정

        time.sleep(10)  # 10초 텀

        # op10 공정 실행 (W1P0)
        op10_data_P0 = machine_operate.op10(body_P0)

        product_key_W1P0 = op10_data_P0['product_key']

        ##### 여기에 웹페이지로 쏴주는 기능 추가 #####

        #################################### W1P0 생산 및 DB 저장 완료 #####################################

        # 다음 공정에 넣기 위한 데이터 가져와서 넣기
        op10_data_P0_from_DB = MySQL_query.get_machine_data_for_process(product_key_W1P0)

        op10_data_list_P0 = []  # P0 재공품 다음공정으로 넣어줄 데이터 저장할 리스트

        op10_l_P0 = op10_data_P0_from_DB[0]['product_size_l']  # 재공품 치수 데이터 가져오기
        op10_w_P0 = op10_data_P0_from_DB[0]['product_size_w']
        op10_h_P0 = op10_data_P0_from_DB[0]['product_size_h']

        op10_timestamp_P0 = op10_data_P0_from_DB[0]['product_test_timestamp']  # op10 P0 끝난시간 가져오기

        op20_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time 새로 생성
        op20_process_time_P0 = round(op20_process_time_P0, 5)

        op20_product_key_P0 = '-' + 'W2' + 'P' + str(0)  # 제품 키 생성

        op10_data_list_P0.append(op20_product_key_P0)  # 2번째 제품 키 - 인덱스 0번
        op10_data_list_P0.append(op10_l_P0)  # 1번 - 길이
        op10_data_list_P0.append(op10_w_P0)  # 2번 - 너비
        op10_data_list_P0.append(op10_h_P0)  # 3번 - 높이
        op10_data_list_P0.append(op10_timestamp_P0)  # 4번 - 전 공정 끝난 시간
        op10_data_list_P0.append(op20_process_time_P0)  # 5번 - 다음 공정 작업할 process_time

        # 병목인지 아닌지 판단 필요없음. 처음 도는 바퀴니까 병목 아님
        op20_start_time_P0 = op10_timestamp_P0 + timedelta(seconds=op20_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
        op10_data_list_P0.append(op20_start_time_P0)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 6번



        body_P1 = []  # P1 제품에 대한 body 값 저장할 리스트

        product_key_W1P1 = '-' + 'W1' + 'P' + str(1)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P1.append(product_key_W1P1)

        body_l_P1 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P1 = round(body_l_P1, 5)
        body_P1.append(body_l_P1)

        body_w_P1 = np.random.normal(200, std)
        body_w_P1 = round(body_w_P1, 5)
        body_P1.append(body_w_P1)

        body_h_P1 = np.random.normal(200, std)
        body_h_P1 = round(body_h_P1, 5)
        body_P1.append(body_h_P1)

        op10_process_time_P1 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P1 = round(op10_process_time_P1, 5)

        body_P1.append(op10_process_time_P1)
        body_P1.append(op10_timestamp_P0)  # 두번째 제품은 P0 끝난시간부터 시작

        time.sleep(10)  # 10초 텀


        # op20 공정 실행 (W2P0)
        op20_data_P0 = machine_operate.op20(op10_data_list_P0)  # <- 앞공정 재공품 받아서 실행
        product_key_W2P0 = op20_data_P0['product_key']

        #################################### W2P0 생산 및 DB 저장 완료 #####################################

        # op10 공정 실행 (W1P1)
        op10_data_P1 = machine_operate.op10(body_P1)
        product_key_W1P1 = op10_data_P1['product_key']

        #################################### W1P1 생산 및 DB 저장 완료 #####################################

        ##### 여기에다가 웹에다가 쏴주는 기능 추가 #####

        # 다음 공정에 넣기 위한 데이터 가져오기
        op20_data_P0_from_DB = MySQL_query.get_machine_data_for_process(product_key_W2P0)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op10_data_P1_from_DB = MySQL_query.get_machine_data_for_process(product_key_W1P1)



        # op20 P0 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op20_data_list_P0 = []

        product_key_W3P0 = '-' + 'W3' + 'P' + str(0)  # 제품 키 생성
        op20_l_P0 = op20_data_P0_from_DB[0]['product_size_l']
        op20_w_P0 = op20_data_P0_from_DB[0]['product_size_w']
        op20_h_P0 = op20_data_P0_from_DB[0]['product_size_h']

        op20_timestamp_P0 = op20_data_P0_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op30_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op30_process_time_P0 = round(op30_process_time_P0, 5)

        op30_start_time_P0 = op20_timestamp_P0 + timedelta(seconds=op30_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임

        op20_data_list_P0.append(product_key_W3P0)
        op20_data_list_P0.append(op20_l_P0)
        op20_data_list_P0.append(op20_w_P0)
        op20_data_list_P0.append(op20_h_P0)
        op20_data_list_P0.append(op20_timestamp_P0)
        op20_data_list_P0.append(op30_process_time_P0)
        op20_data_list_P0.append(op30_start_time_P0)


        # op10 P1 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op10_data_list_P1 = []

        product_key_W2P1 = '-' + 'W2' + 'P' + str(1)  # 제품 키 생성
        op10_l_P1 = op10_data_P1_from_DB[0]['product_size_l']
        op10_w_P1 = op10_data_P1_from_DB[0]['product_size_w']
        op10_h_P1 = op10_data_P1_from_DB[0]['product_size_h']

        op10_timestamp_P1 = op10_data_P1_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op20_process_time_P1 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op20_process_time_P1 = round(op20_process_time_P1, 5)

        op20_start_time_P1 = op10_timestamp_P1 + timedelta(seconds=op20_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임

        op10_data_list_P1.append(product_key_W2P1)
        op10_data_list_P1.append(op10_l_P1)
        op10_data_list_P1.append(op10_w_P1)
        op10_data_list_P1.append(op10_h_P1)
        op10_data_list_P1.append(op10_timestamp_P1)
        op10_data_list_P1.append(op20_process_time_P1)
        op10_data_list_P1.append(op20_start_time_P1)


        body_P2 = []  # P1 제품에 대한 body 값 저장할 리스트

        product_key_W1P2 = '-' + 'W1' + 'P' + str(2)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P2.append(product_key_W1P2)

        body_l_P2 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P2 = round(body_l_P2, 5)
        body_P2.append(body_l_P2)

        body_w_P2 = np.random.normal(200, std)
        body_w_P2 = round(body_w_P2, 5)
        body_P2.append(body_w_P2)

        body_h_P2 = np.random.normal(200, std)
        body_h_P2 = round(body_h_P2, 5)
        body_P2.append(body_h_P2)

        op10_process_time_P2 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P2 = round(op10_process_time_P2, 5)

        body_P2.append(op10_process_time_P2)
        body_P2.append(op10_timestamp_P1)  # 세번째 제품은 P1 끝난시간부터 시작



        # op30, 20, 10 시작

        time.sleep(10)

        # op30 공정 실행 (W3P0)
        op30_data_P0 = machine_operate.op30(op20_data_list_P0)  # <- 앞공정 재공품 받아서 실행
        product_key_W3P0 = op30_data_P0['product_key']

        #################################### W3P0 생산 및 DB 저장 완료 #####################################

        # op20 공정 실행 (W2P0)
        op20_data_P1 = machine_operate.op20(op10_data_list_P1)  # <- 앞공정 재공품 받아서 실행
        product_key_W2P1 = op20_data_P1['product_key']

        #################################### W2P1 생산 및 DB 저장 완료 #####################################

        # op10 공정 실행 (W1P1)
        op10_data_P2 = machine_operate.op10(body_P2)
        product_key_W1P2 = op10_data_P2['product_key']

        #################################### W1P2 생산 및 DB 저장 완료 #####################################

        # 다음 공정에 넣기 위한 데이터 가져오기
        op30_data_P0_from_DB = MySQL_query.get_machine_data_for_process(product_key_W3P0)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op20_data_P1_from_DB = MySQL_query.get_machine_data_for_process(product_key_W2P1)
        # 다음 공정에 넣기 위한 데이터 가져오기
        op10_data_P2_from_DB = MySQL_query.get_machine_data_for_process(product_key_W1P2)


        # op30 P0 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op30_data_list_P0 = []

        product_key_W4P0 = '-' + 'W4' + 'P' + str(0)  # 제품 키 생성
        op30_l_P0 = op30_data_P0_from_DB[0]['product_size_l']
        op30_w_P0 = op30_data_P0_from_DB[0]['product_size_w']
        op30_h_P0 = op30_data_P0_from_DB[0]['product_size_h']

        op30_timestamp_P0 = op30_data_P0_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op40_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op40_process_time_P0 = round(op40_process_time_P0, 5)

        op40_start_time_P0 = op30_timestamp_P0 + timedelta(seconds=op30_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임

        op30_data_list_P0.append(product_key_W4P0)
        op30_data_list_P0.append(op30_l_P0)
        op30_data_list_P0.append(op30_w_P0)
        op30_data_list_P0.append(op30_h_P0)
        op30_data_list_P0.append(op30_timestamp_P0)
        op30_data_list_P0.append(op40_process_time_P0)
        op30_data_list_P0.append(op40_start_time_P0)

        # op20 P1 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op20_data_list_P1 = []

        product_key_W3P1 = '-' + 'W3' + 'P' + str(1)  # 제품 키 생성
        op20_l_P1 = op20_data_P1_from_DB[0]['product_size_l']
        op20_w_P1 = op20_data_P1_from_DB[0]['product_size_w']
        op20_h_P1 = op20_data_P1_from_DB[0]['product_size_h']

        op20_timestamp_P1 = op20_data_P1_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op30_process_time_P1 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op30_process_time_P1 = round(op30_process_time_P1, 5)

        op30_start_time_P1 = op20_timestamp_P1 + timedelta(seconds=op30_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임

        op20_data_list_P1.append(product_key_W3P1)
        op20_data_list_P1.append(op20_l_P1)
        op20_data_list_P1.append(op20_w_P1)
        op20_data_list_P1.append(op20_h_P1)
        op20_data_list_P1.append(op20_timestamp_P1)
        op20_data_list_P1.append(op30_process_time_P1)
        op20_data_list_P1.append(op30_start_time_P1)


        # op10 P1 생산 끝낸 데이터를 다음 공정에 넣을 변수에 저장하기
        op10_data_list_P2 = []

        product_key_W2P2 = '-' + 'W2' + 'P' + str(2)  # 제품 키 생성
        op10_l_P2 = op10_data_P2_from_DB[0]['product_size_l']
        op10_w_P2 = op10_data_P2_from_DB[0]['product_size_w']
        op10_h_P2 = op10_data_P2_from_DB[0]['product_size_h']

        op10_timestamp_P2 = op10_data_P2_from_DB[0]['product_test_timestamp']  # op20 끝난시간

        op20_process_time_P2 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op20_process_time_P2 = round(op20_process_time_P2, 5)

        op20_start_time_P2 = op10_timestamp_P2 + timedelta(seconds=op20_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임

        op10_data_list_P2.append(product_key_W2P2)
        op10_data_list_P2.append(op10_l_P2)
        op10_data_list_P2.append(op10_w_P2)
        op10_data_list_P2.append(op10_h_P2)
        op10_data_list_P2.append(op10_timestamp_P2)
        op10_data_list_P2.append(op20_process_time_P2)
        op10_data_list_P2.append(op20_start_time_P2)


        body_P3 = []  # P1 제품에 대한 body 값 저장할 리스트

        product_key_W1P3 = '-' + 'W1' + 'P' + str(3)  # 첫번째 제품 primary_key 생성 -> machine에서 시간 추가할 예정
        body_P3.append(product_key_W1P3)

        body_l_P2 = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l_P2 = round(body_l_P2, 5)
        body_P3.append(body_l_P2)

        body_w_P2 = np.random.normal(200, std)
        body_w_P2 = round(body_w_P2, 5)
        body_P3.append(body_w_P2)

        body_h_P2 = np.random.normal(200, std)
        body_h_P2 = round(body_h_P2, 5)
        body_P3.append(body_h_P2)

        op10_process_time_P2 = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time_P2 = round(op10_process_time_P2, 5)

        body_P3.append(op10_process_time_P2)
        body_P3.append(op10_timestamp_P2)  # 네번째 제품은 P2 끝난시간부터 시작

        ### 여기까지 다음 공정으로 넣을 4개 재공품들 변수에 저장해둠





















        # 다음 공정에 넣기 위한 데이터 가져와서 넣기
        op10_data_P1 = MySQL_query.get_machine_data_for_process(product_key_W1P1)

        op10_data_list_P0 = []  # P0 재공품 다음공정으로 넣어줄 데이터 저장할 리스트

        op10_l_P0 = op10_data_P0[0]['product_size_l']  # 재공품 치수 데이터 가져오기
        op10_w_P0 = op10_data_P0[0]['product_size_w']
        op10_h_P0 = op10_data_P0[0]['product_size_h']

        op10_timestamp_P0 = op10_data_P0[0]['product_test_timestamp']  # op10 P0 끝난시간 가져오기

        op20_process_time_P0 = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time 새로 생성
        op20_process_time_P0 = round(op20_process_time_P0, 5)

        op20_product_key_P0 = '-' + 'W2' + 'P' + str(0)  # 제품 키 생성

        op10_data_list_P0.append(op20_product_key_P0)  # 2번째 제품 키 - 인덱스 0번
        op10_data_list_P0.append(op10_l_P0)  # 1번 - 길이
        op10_data_list_P0.append(op10_w_P0)  # 2번 - 너비
        op10_data_list_P0.append(op10_h_P0)  # 3번 - 높이
        op10_data_list_P0.append(op10_timestamp_P0)  # 4번 - 전 공정 끝난 시간
        op10_data_list_P0.append(op20_process_time_P0)  # 5번 - 다음 공정 작업할 process_time

        # 병목인지 아닌지 판단 필요없음. 처음 도는 바퀴니까 병목 아님
        op20_start_time_P0 = op10_timestamp_P0 + timedelta(seconds=op20_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
        op10_data_list_P0.append(op20_start_time_P0)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 6번



























        # op10 공정 2번째 제품 시작 (W1P1)
        body = []  # 리스트 값 초기화

        body.append('-' + 'W1' + 'P' + str(1))  # P1 제품 primary_key 생성

        body_l = np.random.normal(200, std)  # body 치수 데이터 생성
        body_l = round(body_l, 5)
        body.append(body_l)

        body_w = np.random.normal(100, std)
        body_w = round(body_w, 5)
        body.append(body_w)

        body_h = np.random.normal(50, std)
        body_h = round(body_h, 5)
        body.append(body_h)

        op10_process_time = np.random.triangular(9, 10, 10)  # process_time 생성
        op10_process_time = round(op10_process_time, 5)
        body.append(op10_process_time)

        body.append(op10_timestamp_P0)  # 시작시간은 1번 제품 끝난 시간

        time.sleep(10)  # 10초 텀

        # P1 제품 공정 시작  (W1P1)
        op10_data_for_product_key = machine_operate.op10(body)  # 공정 돌린 후 데이터 받기
        product_key = op10_data_for_product_key['product_key']  # DB에서 데이터 가져오기 위한 product_key 변수 저장


        # op10에서 끝난 P1 제품을 다음 공정에 넣기 위한 데이터 DB에서 가져오기
        op10_data = MySQL_query.get_quality_data_for_process(product_key)

        op10_data_list = []  # op20에 넣기 위한 값 리스트 초기화

        op10_l = op10_data[0]['product_size_l']
        op10_w = op10_data[0]['product_size_w']
        op10_h = op10_data[0]['product_size_h']

        op10_timestamp = op10_data[0]['product_test_timestamp']  # op10 끝난시간

        op20_process_time = np.random.triangular(9, 10, 10)  # 다음 공정에 넣어줄 process_time
        op20_process_time = round(op20_process_time, 5)

        # if op20_timestamp < op10_timestamp:  # 앞공정에서 더 늦게 끝남 -> 만약 대기행렬에 하나도 없으면 -> 뒷공정이 놀고있다
        #
        #     op20_start_time = op10_timestamp + timedelta(seconds=op10_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
        #     op10_WIP.append(op20_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
        #     op20_data = machine_operate.op20(op10_WIP)  # <- 대기 행렬에 아무것도 없으면 그냥 바로 받아서 실행
        #
        # else:  # 앞공정이 더 빨리 끝나면 -> 뒷공정은 계속 일하는 중 -> 대기행렬에 추가
        #
        #     op20_start_time = op20_timestamp + timedelta(seconds=op10_setup_time)  # 처리한 물품 끝나고 바로 공정 시작 + 셋업타임
        #     op10_WIP.append(op20_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
        #     op20_data = machine_operate.op20(op10_WIP)  # <- 대기 행렬에 아무것도 없으면 그냥 바로 받아서 실행

        op20_start_time = op10_timestamp + timedelta(seconds=op10_setup_time)

        op10_data_list.append('-' + 'W2' + 'P' + str(1))  # W2P1
        op10_data_list.append(op10_l)
        op10_data_list.append(op10_w)
        op10_data_list.append(op10_h)
        op10_data_list.append(op10_timestamp)
        op10_data_list.append(op20_process_time)
        op10_data_list.append(op20_start_time)

















        op10_WIP = []
        op20_data = {}

        product_key = '-' + 'W2' + 'P' + str(i)



        op20_process_time = np.random.triangular(9, 10, 10)
        op20_process_time = round(op20_process_time, 5)

        op10_WIP.append(product_key)
        op10_WIP.append(op10_l)  # <- 돌리고 난 후 데이터 모음에서 결과값 하나씩 가져오기
        op10_WIP.append(op10_w)
        op10_WIP.append(op10_h)
        op10_WIP.append(op10_data['op10_time_stamp'])  # 다음 공정 시작할 시간
        op10_WIP.append(op20_process_time)

        ## op20 시작

        ## 병목인지 아닌지 판단
        op10_timestamp = op10_data['op10_time_stamp']  # op10에서 끝난 시간 가져옴
        op20_start_time = op10_timestamp  # 기본적으로 op20 시작 시간은 op10 끝난 시간

        if op20_timestamp < op10_timestamp:  # 앞공정에서 더 늦게 끝남 -> 만약 대기행렬에 하나도 없으면 -> 뒷공정이 놀고있다

            op20_start_time = op10_timestamp + timedelta(seconds=op10_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
            op10_WIP.append(op20_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op20_data = machine_operate.op20(op10_WIP)  # <- 대기 행렬에 아무것도 없으면 그냥 바로 받아서 실행

        else:  # 앞공정이 더 빨리 끝나면 -> 뒷공정은 계속 일하는 중 -> 대기행렬에 추가

            op20_start_time = op20_timestamp + timedelta(seconds=op10_setup_time)  # 처리한 물품 끝나고 바로 공정 시작 + 셋업타임
            op10_WIP.append(op20_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op20_data = machine_operate.op20(op10_WIP)  # <- 대기 행렬에 아무것도 없으면 그냥 바로 받아서 실행

        op20_timestamp = op20_data['op20_time_stamp']























    for i in range(10):
        quality_predict_data = {}

        total_data = {}

        op10_process_time = np.random.triangular(9, 10, 10)
        op10_process_time = round(op10_process_time, 5)

        op20_process_time = np.random.triangular(9, 10, 10)
        op20_process_time = round(op20_process_time, 5)

        op30_process_time = np.random.triangular(9, 10, 10)
        op30_process_time = round(op30_process_time, 5)

        op40_process_time = np.random.triangular(9, 10, 10)
        op40_process_time = round(op40_process_time, 5)

        op50_process_time = np.random.triangular(9, 10, 10)
        op50_process_time = round(op50_process_time, 5)

        op60_process_time = np.random.triangular(9, 10, 10)
        op60_process_time = round(op60_process_time, 5)

        body = []
        op10_data = {}
        product_key = '-' + 'W1' + 'P' + str(i)
        body.append(product_key)

        body_l = np.random.normal(200, std)
        body_l = round(body_l, 5)
        body.append(body_l)

        body_w = np.random.normal(100, std)
        body_w = round(body_w, 5)
        body.append(body_w)

        body_h = np.random.normal(50, std)
        body_h = round(body_h, 5)
        body.append(body_h)

        body.append(op10_process_time)  # <- 여기까지 body에 생성한 값 넣어주고 공정에 돌리기

        body.append(op10_timestamp)

        ### op 10 시작

        op10_data = machine_operate.op10(body)  # <- 공정 돌리고 난 후 데이터

        quality_predict_data['body_l'] = body_l
        quality_predict_data['body_w'] = body_w
        quality_predict_data['body_h'] = body_h

        wavyfin_l = op10_data['wavyfin_l']
        wavyfin_w = op10_data['wavyfin_w']
        wavyfin_h = op10_data['wavyfin_h']

        quality_predict_data['wavyfin_l'] = wavyfin_l
        quality_predict_data['wavyfin_w'] = wavyfin_w
        quality_predict_data['wavyfin_h'] = wavyfin_h

        op10_l = op10_data['op10_l']
        op10_w = op10_data['op10_w']
        op10_h = op10_data['op10_h']

        quality_predict_data['op10_l'] = op10_l
        quality_predict_data['op10_w'] = op10_w
        quality_predict_data['op10_h'] = op10_h

        op10_electricity = op10_data['op10_electricity']
        op10_process_time = op10_data['op10_process_time']
        op10_test = op10_data['op10_test']

        quality_predict_data['op10_electricity'] = op10_electricity
        quality_predict_data['op10_process_time'] = op10_process_time
        quality_predict_data['op10_test'] = op10_test

        if op10_test == 'OK':
            op10_test = 0
        else:
            op10_test = 1

        op10_WIP = []
        op20_data = {}

        product_key = '-' + 'W2' + 'P' + str(i)

        op10_WIP.append(product_key)
        op10_WIP.append(op10_l)  # <- 돌리고 난 후 데이터 모음에서 결과값 하나씩 가져오기
        op10_WIP.append(op10_w)
        op10_WIP.append(op10_h)
        op10_WIP.append(op10_data['op10_time_stamp'])  # 다음 공정 시작할 시간
        op10_WIP.append(op20_process_time)

        ## op20 시작

        ## 병목인지 아닌지 판단
        op10_timestamp = op10_data['op10_time_stamp']  # op10에서 끝난 시간 가져옴
        op20_start_time = op10_timestamp  # 기본적으로 op20 시작 시간은 op10 끝난 시간

        if op20_timestamp < op10_timestamp:  # 앞공정에서 더 늦게 끝남 -> 만약 대기행렬에 하나도 없으면 -> 뒷공정이 놀고있다

            op20_start_time = op10_timestamp + timedelta(seconds=op10_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
            op10_WIP.append(op20_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op20_data = machine_operate.op20(op10_WIP)  # <- 대기 행렬에 아무것도 없으면 그냥 바로 받아서 실행

        else:  # 앞공정이 더 빨리 끝나면 -> 뒷공정은 계속 일하는 중 -> 대기행렬에 추가

            op20_start_time = op20_timestamp + timedelta(seconds=op10_setup_time)  # 처리한 물품 끝나고 바로 공정 시작 + 셋업타임
            op10_WIP.append(op20_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op20_data = machine_operate.op20(op10_WIP)  # <- 대기 행렬에 아무것도 없으면 그냥 바로 받아서 실행

        op20_timestamp = op20_data['op20_time_stamp']

        pipe1_l = op20_data['pipe1_l']
        pipe1_w = op20_data['pipe1_w']
        pipe1_h = op20_data['pipe1_h']

        quality_predict_data['pipe1_l'] = pipe1_l
        quality_predict_data['pipe1_w'] = pipe1_w
        quality_predict_data['pipe1_h'] = pipe1_h

        op20_l = op20_data['op20_l']
        op20_w = op20_data['op20_w']
        op20_h = op20_data['op20_h']

        quality_predict_data['op20_l'] = op20_l
        quality_predict_data['op20_w'] = op20_w
        quality_predict_data['op20_h'] = op20_h

        op20_electricity = op20_data['op20_electricity']
        op20_process_time = op20_data['op20_process_time']
        op20_test = op20_data['op20_test']

        quality_predict_data['op20_electricity'] = op20_electricity
        quality_predict_data['op20_process_time'] = op20_process_time
        quality_predict_data['op20_test'] = op20_test

        if op20_test == 'OK':
            op20_test = 0
        else:
            op20_test = 1

        op20_WIP = []
        op30_data = {}
        product_key = '-' + 'W3' + 'P' + str(i)  # <- 키 설정

        op20_WIP.append(product_key)
        op20_WIP.append(op20_data['op20_l'])
        op20_WIP.append(op20_data['op20_w'])
        op20_WIP.append(op20_data['op20_h'])
        op20_WIP.append(op20_data['op20_time_stamp'])
        op20_WIP.append(op30_process_time)

        ## op30 시작

        ## 병목인지 아닌지 판단
        op20_timestamp = op20_data['op20_time_stamp']  # op10에서 끝난 시간 가져옴
        op30_start_time = op20_timestamp  # 기본적으로 op30 시작 시간은 op20 끝난 시간

        if op30_timestamp < op20_timestamp:  # 앞공정에서 더 늦게 끝남 -> 만약 대기행렬에 하나도 없으면 -> 뒷공정이 놀고있다

            op30_start_time = op20_timestamp + timedelta(seconds=op20_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
            op20_WIP.append(op30_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op30_data = machine_operate.op30(op20_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        else:  # 앞공정이 더 빨리 끝나면 -> 뒷공정은 계속 일하는 중 -> 대기행렬에 추가

            op30_start_time = op30_timestamp + timedelta(seconds=op20_setup_time)  # 처리한 물품 끝나고 바로 공정 시작 + 셋업타임
            op20_WIP.append(op30_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op30_data = machine_operate.op30(op20_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        op30_timestamp = op30_data['op30_time_stamp']

        pipe2_l = op30_data['pipe2_l']
        pipe2_w = op30_data['pipe2_w']
        pipe2_h = op30_data['pipe2_h']

        quality_predict_data['pipe2_l'] = pipe2_l
        quality_predict_data['pipe2_w'] = pipe2_w
        quality_predict_data['pipe2_h'] = pipe2_h

        op30_l = op30_data['op30_l']
        op30_w = op30_data['op30_w']
        op30_h = op30_data['op30_h']

        quality_predict_data['op30_l'] = op30_l
        quality_predict_data['op30_w'] = op30_w
        quality_predict_data['op30_h'] = op30_h

        op30_electricity = op30_data['op30_electricity']
        op30_process_time = op30_data['op30_process_time']
        op30_test = op30_data['op30_test']

        if op30_test == 'OK':
            op30_test = 0
        else:
            op30_test = 1

        quality_predict_data['op30_electricity'] = op30_electricity
        quality_predict_data['op30_process_time'] = op30_process_time
        quality_predict_data['op30_test'] = op30_test

        # 테스트할 X_test
        X_test = pd.DataFrame({'body_l' : body_l, 'body_w' : body_w, 'body_h' : body_h,
               'wavyfin_l' : wavyfin_l, 'wavyfin_w' : wavyfin_w, 'wavyfin_h' : wavyfin_h,
               'op10_l' : op10_l, 'op10_w' : op10_w, 'op10_h' : op10_h,
               'op10_electricity' : op10_electricity, 'op10_process_time' : op10_process_time,
               'op10_test' : op10_test,

               'pipe1_l' : pipe1_l, 'pipe1_w' : pipe1_w, 'pipe1_h' : pipe1_h,
               'op20_l' : op20_l, 'op20_w' : op20_w, 'op20_h' : op20_h,
               'op20_electricity' : op20_electricity, 'op20_process_time' : op20_process_time,
               'op20_test' : op20_test,

               'pipe2_l' : pipe2_l, 'pipe2_w' : pipe2_w, 'pipe2_h' : pipe2_h,
               'op30_l' : op30_l, 'op30_w' : op30_w, 'op30_h' : op30_h,
               'op30_electricity' : op30_electricity, 'op30_process_time' : op30_process_time,
               'op30_test' : op30_test}, index=[0])

        clf_from_joblib = joblib.load('pretrained_model.pkl')  # 저장했던 모델 불러오기
        pred = clf_from_joblib.predict(X_test)  # 예측
        print(pred)

        op30_WIP = []
        op40_data = {}
        product_key = '-' + 'W4' + 'P' + str(i)

        op30_WIP.append(product_key)
        op30_WIP.append(op30_data['op30_l'])
        op30_WIP.append(op30_data['op30_w'])
        op30_WIP.append(op30_data['op30_h'])
        op30_WIP.append(op30_data['op30_time_stamp'])
        op30_WIP.append(op40_process_time)

        ## op40 시작

        ## 병목인지 아닌지 판단
        op30_timestamp = op30_data['op30_time_stamp']  # op10에서 끝난 시간 가져옴
        op40_start_time = op30_timestamp  # 기본적으로 op40 시작 시간은 op30 끝난 시간

        if op40_timestamp < op30_timestamp:  # 앞공정에서 더 늦게 끝남 -> 만약 대기행렬에 하나도 없으면 -> 뒷공정이 놀고있다

            op40_start_time = op30_timestamp + timedelta(seconds=op30_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
            op30_WIP.append(op40_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op40_data = machine_operate.op40(op30_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        else:  # 앞공정이 더 빨리 끝나면 -> 뒷공정은 계속 일하는 중 -> 대기행렬에 추가

            op40_start_time = op40_timestamp + timedelta(seconds=op30_setup_time)  # 처리한 물품 끝나고 바로 공정 시작 + 셋업타임
            op30_WIP.append(op40_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op40_data = machine_operate.op40(op30_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        op40_timestamp = op40_data['op40_time_stamp']

        op40_WIP = []
        op50_data = {}
        product_key = '-' + 'W5' + 'P' + str(i)

        op40_WIP.append(product_key)
        op40_WIP.append(op40_data['op40_l'])
        op40_WIP.append(op40_data['op40_w'])
        op40_WIP.append(op40_data['op40_h'])
        op40_WIP.append(op40_data['op40_time_stamp'])
        op40_WIP.append(op50_process_time)

        ## op 50 시작

        ## 병목인지 아닌지 판단
        op40_timestamp = op40_data['op40_time_stamp']  # op10에서 끝난 시간 가져옴
        op50_start_time = op40_timestamp  # 기본적으로 op50 시작 시간은 op40 끝난 시간

        if op50_timestamp < op40_timestamp:  # 앞공정에서 더 늦게 끝남 -> 만약 대기행렬에 하나도 없으면 -> 뒷공정이 놀고있다

            op50_start_time = op40_timestamp + timedelta(seconds=op40_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
            op40_WIP.append(op50_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op50_data = machine_operate.op50(op40_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        else:  # 앞공정이 더 빨리 끝나면 -> 뒷공정은 계속 일하는 중 -> 대기행렬에 추가

            op50_start_time = op50_timestamp + timedelta(seconds=op40_setup_time)  # 처리한 물품 끝나고 바로 공정 시작 + 셋업타임
            op40_WIP.append(op50_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op50_data = machine_operate.op50(op40_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        op50_timestamp = op50_data['op50_time_stamp']

        op50_WIP = []
        op60_data = {}
        product_key = '-' + 'W6' + 'P' + str(i)

        op50_WIP.append(product_key)
        op50_WIP.append(op50_data['op50_l'])
        op50_WIP.append(op50_data['op50_w'])
        op50_WIP.append(op50_data['op50_h'])
        op50_WIP.append(op50_data['op50_time_stamp'])
        op50_WIP.append(op60_process_time)

        ## op60 시작

        ## 병목인지 아닌지 판단
        op50_timestamp = op50_data['op50_time_stamp']  # op10에서 끝난 시간 가져옴
        op60_start_time = op50_timestamp  # 기본적으로 op60 시작 시간은 op50 끝난 시간

        if op60_timestamp < op50_timestamp:  # 앞공정에서 더 늦게 끝남 -> 만약 대기행렬에 하나도 없으면 -> 뒷공정이 놀고있다

            op60_start_time = op50_timestamp + timedelta(seconds=op50_setup_time)  # 앞공정 끝난시간이 뒷공정 시작시간 + 셋업타임
            op50_WIP.append(op60_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op60_data = machine_operate.op60(op50_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        else:  # 앞공정이 더 빨리 끝나면 -> 뒷공정은 계속 일하는 중 -> 대기행렬에 추가

            op60_start_time = op60_timestamp + timedelta(seconds=op50_setup_time)  # 처리한 물품 끝나고 바로 공정 시작 + 셋업타임
            op50_WIP.append(op60_start_time)  # 재공품 정보에 시작해야할 시간 저장 / 인덱스 5번
            op60_data = machine_operate.op60(op50_WIP)  # <- 시작해야하는 시간 정보 받아서 다음공정 실행

        op60_timestamp = op60_data['op60_time_stamp']

        op10_data = dict(op10_data, **op20_data)
        op10_data = dict(op10_data, **op30_data)
        op10_data = dict(op10_data, **op40_data)
        op10_data = dict(op10_data, **op50_data)
        op10_data = dict(op10_data, **op60_data)
        total_data = dict(total_data, **op10_data)

        item_sink.append(total_data)
        result_df = pd.DataFrame(item_sink)
        result_df = result_df.set_index('product_key')

    return total_data