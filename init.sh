#!/usr/bin/env bash
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

read -p "Enter base directory: " BASE_DIR

cat <<EOF > setting_for_sda/path_setting.py
path_list = {
    "data_root_dir": "$BASE_DIR",

    ## topic modeling result dirs
    "bert_monthly_data_dir" : "$BASE_DIR/result/bert_based/run_id_0/data",
    # 2021년 01 월부터의 데이터
    "bert_monthly_data_dir_2" : "$BASE_DIR/result/bert_based/run_id_2/data",
    # snapshot2 data
    "bert_monthly_data_dir_3" : "$BASE_DIR/result/bert_based/run_id_3/data",

    ##tag result dirs
    "tag_monthly_data_dir"    : "$BASE_DIR/result/tag/run_id_0/data",
    #2021.11 ~ 2024.11
    "tag_monthly_data_dir_2"  : "$BASE_DIR/result/tag/run_id_2/data",  

    "tag_monthly_data_dir_2_py"  : "$BASE_DIR/result/tag/run_id_2/python/data",
    "tag_monthly_data_dir_2_cpp"  : "$BASE_DIR/result/tag/run_id_2/cpp/data",

    ##LDA result dirs
    "lda_monthly_data_dir" : "$BASE_DIR/result/lda/run_id_1/data",

    ##topic.tag X Difficulty result dirs
    "bert_difficulty_data_dir" : "$BASE_DIR/result/bert_based/difficulty_annotated/data",
    "lda_difficulty_data_dir" : "$BASE_DIR/result/lda/difficulty_annotated/data",
    "tag_difficulty_data_dir" : "$BASE_DIR/result/tag/difficulty_annotated/data",

}
EOF

echo "path_setting.py created"