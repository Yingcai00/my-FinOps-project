package com.finops.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.finops.mapper.ProductCostRelationMapper;
import com.finops.mapper.ProductMapper;
import com.finops.model.Product;
import com.finops.model.ProductCostRelation;
import com.finops.service.ProductService;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.time.LocalDateTime;
import java.util.List;

@Service
public class ProductServiceImpl extends ServiceImpl<ProductMapper, Product> implements ProductService {

    @Resource
    private ProductCostRelationMapper productCostRelationMapper;

    @Override
    @Transactional
    public boolean addProductWithCostRelations(Product product, List<ProductCostRelation> relations) {
        // 保存产品
        product.setCreatedTime(LocalDateTime.now());
        product.setUpdatedTime(LocalDateTime.now());
        if (!save(product)) return false;

        // 保存产品成本关联
        for (ProductCostRelation relation : relations) {
            relation.setProductId(product.getId());
            relation.setCreatedTime(LocalDateTime.now());
            relation.setUpdatedTime(LocalDateTime.now());
            productCostRelationMapper.insert(relation);
        }

        return true;
    }

    @Override
    @Transactional
    public boolean updateProductWithCostRelations(Product product, List<ProductCostRelation> relations) {
        // 更新产品
        product.setUpdatedTime(LocalDateTime.now());
        if (!updateById(product)) return false;

        // 删除旧的关联
        productCostRelationMapper.delete(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <ProductCostRelation>lambdaQuery().eq(ProductCostRelation::getProductId, product.getId())
        );

        // 保存新的关联
        for (ProductCostRelation relation : relations) {
            relation.setProductId(product.getId());
            relation.setCreatedTime(LocalDateTime.now());
            relation.setUpdatedTime(LocalDateTime.now());
            productCostRelationMapper.insert(relation);
        }

        return true;
    }

    @Override
    public List<ProductCostRelation> getProductCostRelations(Long productId) {
        return productCostRelationMapper.selectList(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <ProductCostRelation>lambdaQuery().eq(ProductCostRelation::getProductId, productId)
        );
    }

    @Override
    public boolean calculateUnitPrice(String month) {
        // 这里实现产品单价计算的逻辑
        // 实际项目中需要根据成本项和定价公式计算
        return true;
    }

}
