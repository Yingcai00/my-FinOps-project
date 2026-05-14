package com.finops.model;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("bill_items")
public class BillItem implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    private Long id;

    private Long billId;

    private Long productId;

    private BigDecimal amount;

    private BigDecimal unitPrice;

    private BigDecimal subtotal;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

}
