@router.post("/bill", response_model=BillResponse)
def create_bill(bill_in: BillCreate, db: Session = Depends(get_db)):
    total_cost = 0
    bill_details_list = []

    # tạo Bill
    bill = Bill(user_id=bill_in.user_id)
    db.add(bill)
    db.commit()       # commit 1 lần để sinh bill_id
    db.refresh(bill)

    # xử lý từng item
    for item in bill_in.items:
        fruit = db.query(Fruit).filter(Fruit.id == item.fruit_id).first()
        if not fruit:
            raise HTTPException(status_code=404, detail=f"Fruit ID {item.fruit_id} not found")

        price = fruit.price * item.weight
        total_cost += price

        detail = BillDetail(
            bill_id=bill.bill_id,
            fruit_id=item.fruit_id,
            weight=item.weight,
            price=fruit.price
        )
        db.add(detail)
        bill_details_list.append(detail)

    db.commit()  # commit tất cả detail cùng lúc
    for detail in bill_details_list:
        db.refresh(detail)

    # prepare response
    response_details = [
        BillDetailResponse(
            detail_id=d.detail_id,
            fruit_id=d.fruit_id,
            fruit_name=db.query(Fruit).filter(Fruit.id == d.fruit_id).first().name,
            weight=d.weight,
            price=d.price
        )
        for d in bill_details_list
    ]

    return BillResponse(
        bill_id=bill.bill_id,
        date=bill.date,
        user_id=bill.user_id,
        total_cost=total_cost,
        bill_details=response_details
    )
