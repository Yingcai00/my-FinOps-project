package com.finops.controller;

import com.finops.model.UsageRecord;
import com.finops.service.UsageRecordService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/usage")
public class UsageController {

    @Resource
    private UsageRecordService usageRecordService;

    @PostMapping
    public Map<String, Object> addUsageRecord(@RequestBody UsageRecord usageRecord) {
        boolean success = usageRecordService.save(usageRecord);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("id", usageRecord.getId())
        );
    }

    @PostMapping("/batch")
    public Map<String, Object> batchAddUsageRecords(@RequestBody List<UsageRecord> usageRecords) {
        boolean success = usageRecordService.batchImport(usageRecords);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

    @GetMapping
    public Map<String, Object> getUsageRecords(
            @RequestParam(required = false) String month,
            @RequestParam(required = false) Long departmentId,
            @RequestParam(required = false) Long productId) {
        List<UsageRecord> usageRecords;
        if (month != null && departmentId != null) {
            usageRecords = usageRecordService.getByMonthAndDepartment(month, departmentId);
        } else if (month != null && productId != null) {
            usageRecords = usageRecordService.getByMonthAndProduct(month, productId);
        } else {
            usageRecords = usageRecordService.list();
        }
        return Map.of(
                "code", 200,
                "data", usageRecords
        );
    }

}
