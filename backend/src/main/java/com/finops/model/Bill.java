package com.finops.model;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@TableName("bills")
public class Bill implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    private Long id;

    private Long departmentId;

    private String month;

    private BigDecimal totalAmount;

    private String status;

    private Long creatorId;

    private Long approverId;

    private LocalDateTime approveTime;

    private String remark;

    private LocalDateTime createdTime;

    private LocalDateTime updatedTime;

}
