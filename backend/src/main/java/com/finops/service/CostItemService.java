package com.finops.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.finops.model.CostItem;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface CostItemService extends IService<CostItem> {

    boolean batchImport(MultipartFile file);

    boolean syncFromAssetSystem();

    boolean calculateCost(String month);

    List<CostItem> getByMonth(String month);

    List<CostItem> getByCategory(String category);

}
