package com.finops.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.finops.model.Product;
import com.finops.model.ProductCostRelation;

import java.util.List;

public interface ProductService extends IService<Product> {

    boolean addProductWithCostRelations(Product product, List<ProductCostRelation> relations);

    boolean updateProductWithCostRelations(Product product, List<ProductCostRelation> relations);

    List<ProductCostRelation> getProductCostRelations(Long productId);

    boolean calculateUnitPrice(String month);

}
