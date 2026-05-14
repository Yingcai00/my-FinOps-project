package com.finops.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.finops.model.Configuration;

public interface ConfigurationService extends IService<Configuration> {

    String getConfigValue(String key);

    boolean updateConfigValue(String key, String value);

}
