package com.finops.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.finops.mapper.BillItemMapper;
import com.finops.mapper.BillMapper;
import com.finops.model.Bill;
import com.finops.model.BillItem;
import com.finops.service.BillService;
import com.finops.service.UsageRecordService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class BillServiceImpl extends ServiceImpl<BillMapper, Bill> implements BillService {

    @Resource
    private BillItemMapper billItemMapper;

    @Resource
    private UsageRecordService usageRecordService;

    @Override
    @Transactional
    public Long generateDepartmentBill(String month, Long departmentId) {
        // 获取部门当月的用量记录
        List<com.finops.model.UsageRecord> usageRecords = usageRecordService.getByMonthAndDepartment(month, departmentId);
        if (usageRecords.isEmpty()) return null;

        // 创建账单
        Bill bill = new Bill();
        bill.setDepartmentId(departmentId);
        bill.setMonth(month);
        bill.setStatus("待审核");
        bill.setCreatedTime(LocalDateTime.now());
        bill.setUpdatedTime(LocalDateTime.now());

        // 计算总金额并保存账单
        BigDecimal totalAmount = calculateBillItems(bill, usageRecords);
        bill.setTotalAmount(totalAmount);
        save(bill);

        return bill.getId();
    }

    private BigDecimal calculateBillItems(Bill bill, List<com.finops.model.UsageRecord> usageRecords) {
        // 按产品分组计算费用
        // 实际项目中需要根据产品定价和用量计算费用
        BigDecimal totalAmount = BigDecimal.ZERO;

        // 这里简化处理，实际项目中需要更复杂的计算逻辑
        for (com.finops.model.UsageRecord record : usageRecords) {
            BillItem billItem = new BillItem();
            billItem.setBillId(bill.getId());
            billItem.setProductId(record.getProductId());
            billItem.setAmount(record.getAmount());
            billItem.setUnitPrice(BigDecimal.valueOf(100)); // 这里应该根据产品定价获取
            billItem.setSubtotal(billItem.getAmount().multiply(billItem.getUnitPrice()));
            billItem.setCreatedTime(LocalDateTime.now());
            billItem.setUpdatedTime(LocalDateTime.now());

            billItemMapper.insert(billItem);
            totalAmount = totalAmount.add(billItem.getSubtotal());
        }

        return totalAmount;
    }

    @Override
    public boolean approveBill(Long billId, Long approverId) {
        Bill bill = getById(billId);
        if (bill == null) return false;

        bill.setStatus("已审核");
        bill.setApproverId(approverId);
        bill.setApproveTime(LocalDateTime.now());
        bill.setUpdatedTime(LocalDateTime.now());

        return updateById(bill);
    }

    @Override
    public List<BillItem> getBillItems(Long billId) {
        return billItemMapper.selectList(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <BillItem>lambdaQuery().eq(BillItem::getBillId, billId)
        );
    }

    @Override
    public List<Bill> getByMonth(String month) {
        return baseMapper.selectList(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <Bill>lambdaQuery().eq(Bill::getMonth, month)
        );
    }

}
