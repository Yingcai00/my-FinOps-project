package com.finops.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.finops.mapper.ConfigurationMapper;
import com.finops.model.Configuration;
import com.finops.service.ConfigurationService;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class ConfigurationServiceImpl extends ServiceImpl<ConfigurationMapper, Configuration> implements ConfigurationService {

    @Override
    public String getConfigValue(String key) {
        Configuration config = baseMapper.selectOne(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <Configuration>lambdaQuery().eq(Configuration::getKey, key)
        );
        return config != null ? config.getValue() : null;
    }

    @Override
    public boolean updateConfigValue(String key, String value) {
        Configuration config = baseMapper.selectOne(
                com.baomidou.mybatisplus.core.conditions.query.QueryWrapper.
                        <Configuration>lambdaQuery().eq(Configuration::getKey, key)
        );

        if (config != null) {
            config.setValue(value);
            config.setUpdatedTime(LocalDateTime.now());
            return updateById(config);
        } else {
            config = new Configuration();
            config.setKey(key);
            config.setValue(value);
            config.setCreatedTime(LocalDateTime.now());
            config.setUpdatedTime(LocalDateTime.now());
            return save(config);
        }
    }

}
