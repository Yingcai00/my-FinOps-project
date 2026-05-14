package com.finops.controller;

import com.finops.model.CostItem;
import com.finops.service.CostItemService;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/cost")
public class CostController {

    @Resource
    private CostItemService costItemService;

    @PostMapping("/items")
    public Map<String, Object> batchImport(@RequestParam("file") MultipartFile file) {
        boolean success = costItemService.batchImport(file);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success, "count", 0)
        );
    }

    @PostMapping("/items/sync")
    public Map<String, Object> syncFromAssetSystem(@RequestBody Map<String, String> request) {
        boolean success = costItemService.syncFromAssetSystem();
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success, "count", 0)
        );
    }

    @GetMapping("/items")
    public Map<String, Object> getCostItems(
            @RequestParam(required = false) String month,
            @RequestParam(required = false) String category) {
        List<CostItem> costItems;
        if (month != null) {
            costItems = costItemService.getByMonth(month);
        } else if (category != null) {
            costItems = costItemService.getByCategory(category);
        } else {
            costItems = costItemService.list();
        }
        return Map.of(
                "code", 200,
                "data", costItems
        );
    }

    @PostMapping("/calculate")
    public Map<String, Object> calculateCost(@RequestBody Map<String, String> request) {
        String month = request.get("month");
        boolean success = costItemService.calculateCost(month);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

    @PostMapping("/items/add")
    public Map<String, Object> addCostItem(@RequestBody CostItem costItem) {
        boolean success = costItemService.save(costItem);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

    @PutMapping("/items/{id}")
    public Map<String, Object> updateCostItem(@PathVariable Long id, @RequestBody CostItem costItem) {
        costItem.setId(id);
        boolean success = costItemService.updateById(costItem);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

    @DeleteMapping("/items/{id}")
    public Map<String, Object> deleteCostItem(@PathVariable Long id) {
        boolean success = costItemService.removeById(id);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

}
