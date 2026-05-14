package com.finops.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.finops.mapper.UsageRecordMapper;
import com.finops.model.UsageRecord;
import com.finops.service.UsageRecordService;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class UsageRecordServiceImpl extends ServiceImpl<UsageRecordMapper, UsageRecord> implements UsageRecordService {

    @Override
    public boolean batchImport(List<UsageRecord> usageRecords) {
        for (UsageRecord record : usageRecords) {
            record.setCreatedTime(LocalDateTime.now());
            record.setUpdatedTime(LocalDateTime.now());
        }
        return saveBatch(usageRecords);
    }

    @Override
    public List<UsageRecord> getByMonthAndDepartment(String month, Long departmentId) {
        return baseMapper.selectList(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <UsageRecord>lambdaQuery()
                                .eq(UsageRecord::getUsageMonth, month)
                                .eq(UsageRecord::getDepartmentId, departmentId)
        );
    }

    @Override
    public List<UsageRecord> getByMonthAndProduct(String month, Long productId) {
        return baseMapper.selectList(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <UsageRecord>lambdaQuery()
                                .eq(UsageRecord::getUsageMonth, month)
                                .eq(UsageRecord::getProductId, productId)
        );
    }

}
