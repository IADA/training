<?php
// �t�@�C�������擾���āA���j�[�N�ȃt�@�C�����ɕύX
$file_name = $_FILES['upfile']['name'];
$uniq_file_name = date("YmdHis") . "_" . $file_name;

// ���Ƀt�@�C�����A�b�v���[�h����Ă���ꏊ�̃p�X���擾
$tmp_path = $_FILES['upfile']['tmp_name'];

// �ۑ���̃p�X��ݒ�
$upload_path = './upload/';

if (is_uploaded_file($tmp_path)) {
  // ���̃A�b�v���[�h�ꏊ����ۑ���Ƀt�@�C�����ړ�
  if (move_uploaded_file($tmp_path, $upload_path . $uniq_file_name)) {
    // �t�@�C�����Ǐo�\�ɂȂ�悤�ɃA�N�Z�X������ύX
    chmod($upload_path . $uniq_file_name, 0644);

    echo $file_name . "���A�b�t�K���[�g�J���܂����B";
    echo "<br><a href='sample.html'><- TOP�֖߂�</a>";
  } else {
    echo "Error:�A�b�t�K���[�g�J�Ɏ��s���܂����B";
  }
} else {
  echo "Error:�摜��������܂���B";
}
?>