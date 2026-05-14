package com.finops.controller;

import com.finops.service.ConfigurationService;
import org.springframework.web.bind.annotation.*;

import javax.annotation.Resource;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/config")
public class ConfigController {

    @Resource
    private ConfigurationService configurationService;

    @GetMapping("/{key}")
    public Map<String, Object> getConfig(@PathVariable String key) {
        String value = configurationService.getConfigValue(key);
        return Map.of(
                "code", 200,
                "data", Map.of("key", key, "value", value)
        );
    }

    @PutMapping("/{key}")
    public Map<String, Object> updateConfig(@PathVariable String key, @RequestBody Map<String, String> request) {
        String value = request.get("value");
        boolean success = configurationService.updateConfigValue(key, value);
        return Map.of(
                "code", success ? 200 : 500,
                "data", Map.of("success", success)
        );
    }

}
