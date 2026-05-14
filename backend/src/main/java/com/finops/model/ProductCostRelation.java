package com.finops.model;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("product_cost_relations")
public class ProductCostRelation implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    private Long id;

    private Long productId;

    private Long costItemId;

    private BigDecimal ratio;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

}
