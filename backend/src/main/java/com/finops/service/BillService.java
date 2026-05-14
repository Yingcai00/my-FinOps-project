package com.finops.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.finops.model.Bill;
import com.finops.model.BillItem;

import java.util.List;

public interface BillService extends IService<Bill> {

    Long generateDepartmentBill(String month, Long departmentId);

    boolean approveBill(Long billId, Long approverId);

    List<BillItem> getBillItems(Long billId);

    List<Bill> getByMonth(String month);

}
