package com.finops.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.finops.model.UsageRecord;

import java.util.List;

public interface UsageRecordService extends IService<UsageRecord> {

    boolean batchImport(List<UsageRecord> usageRecords);

    List<UsageRecord> getByMonthAndDepartment(String month, Long departmentId);

    List<UsageRecord> getByMonthAndProduct(String month, Long productId);

}
