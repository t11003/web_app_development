from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.record import RecordModel

# 建立一個 Blueprint 來管理收支紀錄相關路由
bp = Blueprint('records', __name__)

@bp.route('/')
def index():
    """
    [GET] 首頁
    顯示目前總餘額以及近期的收支歷史紀錄
    """
    pass

@bp.route('/records/new', methods=['GET'])
def new_record():
    """
    [GET] 新增紀錄頁面
    顯示填寫收支資料的表單
    """
    pass

@bp.route('/records', methods=['POST'])
def create_record():
    """
    [POST] 送出新增紀錄
    接收表單資料並寫入資料庫，完成後導回首頁
    """
    pass

@bp.route('/records/<int:record_id>/edit', methods=['GET'])
def edit_record(record_id):
    """
    [GET] 編輯紀錄頁面
    顯示帶有原始資料的編輯表單頁面
    """
    pass

@bp.route('/records/<int:record_id>/update', methods=['POST'])
def update_record(record_id):
    """
    [POST] 更新紀錄
    接收更新資料並寫入資料庫，完成後導回首頁
    """
    pass

@bp.route('/records/<int:record_id>/delete', methods=['POST'])
def delete_record(record_id):
    """
    [POST] 刪除紀錄
    將指定 ID 的收支紀錄從資料庫中刪除，並導回首頁
    """
    pass
