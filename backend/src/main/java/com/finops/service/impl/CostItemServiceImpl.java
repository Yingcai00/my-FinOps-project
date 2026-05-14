package com.finops.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.finops.mapper.CostItemMapper;
import com.finops.model.CostItem;
import com.finops.service.CostItemService;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.InputStream;
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class CostItemServiceImpl extends ServiceImpl<CostItemMapper, CostItem> implements CostItemService {

    @Override
    public boolean batchImport(MultipartFile file) {
        try (InputStream inputStream = file.getInputStream();
             Workbook workbook = new XSSFWorkbook(inputStream)) {

            Sheet sheet = workbook.getSheetAt(0);
            List<CostItem> costItems = new ArrayList<>();

            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
                Row row = sheet.getRow(i);
                if (row == null) continue;

                CostItem costItem = new CostItem();
                costItem.setName(getCellValue(row.getCell(0)));
                costItem.setCategory(getCellValue(row.getCell(1)));
                costItem.setSubcategory(getCellValue(row.getCell(2)));
                costItem.setUnitPrice(new BigDecimal(getCellValue(row.getCell(3))));
                costItem.setDepreciationMonths(Integer.parseInt(getCellValue(row.getCell(4))));
                costItem.setQuantity(Integer.parseInt(getCellValue(row.getCell(5))));
                costItem.setUnit(getCellValue(row.getCell(6)));
                costItem.setShareType(getCellValue(row.getCell(7)));
                costItem.setRegion(getCellValue(row.getCell(8)));
                costItem.setShareDimension(getCellValue(row.getCell(9)));
                costItem.setDescription(getCellValue(row.getCell(10)));
                costItem.setCostCode(getCellValue(row.getCell(11)));
                costItem.setDataSource(getCellValue(row.getCell(12)));
                costItem.setCostMonth(getCellValue(row.getCell(13)));
                costItem.setCreatedTime(LocalDateTime.now());
                costItem.setUpdatedTime(LocalDateTime.now());

                costItems.add(costItem);
            }

            return saveBatch(costItems);
        } catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }

    @Override
    public boolean syncFromAssetSystem() {
        // 这里实现从资产系统同步数据的逻辑
        // 实际项目中需要调用资产系统的API获取数据
        return true;
    }

    @Override
    public boolean calculateCost(String month) {
        List<CostItem> costItems = getByMonth(month);
        if (costItems.isEmpty()) return false;

        // 计算折旧月价和月成本
        for (CostItem item : costItems) {
            BigDecimal depreciationMonthlyPrice = item.getUnitPrice()
                    .divide(new BigDecimal(item.getDepreciationMonths()), 2, BigDecimal.ROUND_HALF_UP);
            item.setDepreciationMonthlyPrice(depreciationMonthlyPrice);

            BigDecimal monthlyCost = depreciationMonthlyPrice.multiply(new BigDecimal(item.getQuantity()));
            item.setMonthlyCost(monthlyCost);
            item.setUpdatedTime(LocalDateTime.now());
        }

        // 计算公摊比例和公摊后成本
        calculateShareRatio(costItems);

        return updateBatchById(costItems);
    }

    private void calculateShareRatio(List<CostItem> costItems) {
        // 按成本类别分组计算公摊比例
        // 实际项目中需要更复杂的计算逻辑
    }

    @Override
    public List<CostItem> getByMonth(String month) {
        return baseMapper.selectList(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <CostItem>lambdaQuery().eq(CostItem::getCostMonth, month)
        );
    }

    @Override
    public List<CostItem> getByCategory(String category) {
        return baseMapper.selectList(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <CostItem>lambdaQuery().eq(CostItem::getCategory, category)
        );
    }

    private String getCellValue(Cell cell) {
        if (cell == null) return "";
        switch (cell.getCellType()) {
            case STRING:
                return cell.getStringCellValue();
            case NUMERIC:
                return String.valueOf(cell.getNumericCellValue());
            case BOOLEAN:
                return String.valueOf(cell.getBooleanCellValue());
            default:
                return "";
        }
    }

}
