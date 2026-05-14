package com.finops.controller;

import com.finops.model.Product;
import com.finops.model.ProductCostRelation;
import com.finops.service.ProductService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/products")
public class ProductController {

    @Resource
    private ProductService productService;

    @PostMapping
    public Map<String, Object> addProduct(@RequestBody Map<String, Object> request) {
        Product product = new Product();
        product.setName((String) request.get("name"));
        product.setCode((String) request.get("code"));
        product.setDescription((String) request.get("description"));
        product.setBottleneckResource((String) request.get("bottleneckResource"));
        product.setPricingFormula((String) request.get("pricingFormula"));
        product.setEnabled(true);

        List<Map<String, Object>> relations = (List<Map<String, Object>>) request.get("costItems");
        List<ProductCostRelation> productCostRelations = relations.stream().map(item -> {
            ProductCostRelation relation = new ProductCostRelation();
            relation.setCostItemId(Long.parseLong(item.get("costItemId").toString()));
            relation.setRatio(new java.math.BigDecimal(item.get("ratio").toString()));
            return relation;
        }).toList();

        boolean success = productService.addProductWithCostRelations(product, productCostRelations);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("id", product.getId(), "name", product.getName())
        );
    }

    @GetMapping
    public Map<String, Object> getProducts() {
        List<Product> products = productService.list();
        return Map.of(
                "code", 200,
                "data", products
        );
    }

    @GetMapping("/{id}")
    public Map<String, Object> getProduct(@PathVariable Long id) {
        Product product = productService.getById(id);
        List<ProductCostRelation> relations = productService.getProductCostRelations(id);
        return Map.of(
                "code", 200,
                "data", Map.of(
                        "product", product,
                        "costRelations", relations
                )
        );
    }

    @PutMapping("/{id}")
    public Map<String, Object> updateProduct(@PathVariable Long id, @RequestBody Map<String, Object> request) {
        Product product = new Product();
        product.setId(id);
        product.setName((String) request.get("name"));
        product.setCode((String) request.get("code"));
        product.setDescription((String) request.get("description"));
        product.setBottleneckResource((String) request.get("bottleneckResource"));
        product.setPricingFormula((String) request.get("pricingFormula"));

        List<Map<String, Object>> relations = (List<Map<String, Object>>) request.get("costItems");
        List<ProductCostRelation> productCostRelations = relations.stream().map(item -> {
            ProductCostRelation relation = new ProductCostRelation();
            relation.setCostItemId(Long.parseLong(item.get("costItemId").toString()));
            relation.setRatio(new java.math.BigDecimal(item.get("ratio").toString()));
            return relation;
        }).toList();

        boolean success = productService.updateProductWithCostRelations(product, productCostRelations);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

    @DeleteMapping("/{id}")
    public Map<String, Object> deleteProduct(@PathVariable Long id) {
        boolean success = productService.removeById(id);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

    @PostMapping("/calculate")
    public Map<String, Object> calculateUnitPrice(@RequestBody Map<String, String> request) {
        String month = request.get("month");
        boolean success = productService.calculateUnitPrice(month);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

}
