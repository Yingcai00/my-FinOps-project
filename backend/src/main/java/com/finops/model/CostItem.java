package com.finops.model;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("cost_items")
public class CostItem implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    private Long id;

    private String name;

    private String category;

    private String subcategory;

    private BigDecimal unitPrice;

    private Integer depreciationMonths;

    private Integer quantity;

    private String unit;

    private BigDecimal monthlyCost;

    private BigDecimal depreciationMonthlyPrice;

    private String shareType;

    private String region;

    private String shareDimension;

    private String description;

    private String costCode;

    private String dataSource;

    private Integer cpuTotal;

    private Integer memoryTotal;

    private Integer storageTotal;

    private Integer trafficTotal;

    private String costMonth;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

}
