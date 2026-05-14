package com.finops.controller;

import com.finops.model.Bill;
import com.finops.model.BillItem;
import com.finops.service.BillService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/bills")
public class BillController {

    @Resource
    private BillService billService;

    @PostMapping
    public Map<String, Object> generateBill(@RequestBody Map<String, Object> request) {
        String month = (String) request.get("month");
        Long departmentId = Long.parseLong(request.get("departmentId").toString());
        Long billId = billService.generateDepartmentBill(month, departmentId);
        return Map.of(
                "code", billId != null ? 200 : 500,
                "data", Map.of("billId", billId)
        );
    }

    @GetMapping
    public Map<String, Object> getBills(@RequestParam(required = false) String month) {
        List<Bill> bills;
        if (month != null) {
            bills = billService.getByMonth(month);
        } else {
            bills = billService.list();
        }
        return Map.of(
                "code", 200,
                "data", bills
        );
    }

    @GetMapping("/{id}")
    public Map<String, Object> getBill(@PathVariable Long id) {
        Bill bill = billService.getById(id);
        List<BillItem> items = billService.getBillItems(id);
        return Map.of(
                "code", 200,
                "data", Map.of(
                        "bill", bill,
                        "items", items
                )
        );
    }

    @PostMapping("/{id}/approve")
    public Map<String, Object> approveBill(@PathVariable Long id, @RequestBody Map<String, Object> request) {
        Long approverId = Long.parseLong(request.get("approverId").toString());
        boolean success = billService.approveBill(id, approverId);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

}
