package water.util;

import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.logging.log4j.core.Filter;
import org.apache.logging.log4j.core.config.Configurator;
import org.apache.logging.log4j.core.config.builder.api.*;
import org.apache.logging.log4j.core.config.builder.impl.BuiltConfiguration;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

public class LoggerBackend {

    public static final Level[] L4J_LVLS = { Level.FATAL, Level.ERROR, Level.WARN, Level.INFO, Level.DEBUG, Level.TRACE };
    public static final org.apache.logging.log4j.Level[] L4J_LOGGING_LVLS = {
            org.apache.logging.log4j.Level.FATAL,
            org.apache.logging.log4j.Level.ERROR,
            org.apache.logging.log4j.Level.WARN,
            org.apache.logging.log4j.Level.INFO,
            org.apache.logging.log4j.Level.DEBUG,
            org.apache.logging.log4j.Level.TRACE
    };

    public int _level;
    public String _prefix;
    public String _maxLogFileSize;
    public boolean _launchedWithHadoopJar;
    public boolean _haveInheritedLog4jConfiguration;
    public Function<String, String> _getLogFilePath;

    public Logger createLog4j() {
        reconfigureLog4J();
        return Logger.getLogger("water.default");
    }

    public void reconfigureLog4J() {
        ConfigurationBuilder<BuiltConfiguration> builder = ConfigurationBuilderFactory.newConfigurationBuilder();
        builder.setStatusLevel(L4J_LOGGING_LVLS[_level]);
        builder.setConfigurationName("H2OLogConfiguration");
        
        // configure appenders:
        String patternTail = _prefix + " %10.10t %5.5p %c: %m%n";
        String pattern = "%d{MM-dd HH:mm:ss.SSS} " + patternTail;

        LayoutComponentBuilder layoutComponentBuilder = builder.newLayout("PatternLayout").addAttribute("pattern", pattern);

        builder.add(builder.newAppender("Console", "Console")
                .addAttribute("target", "SYSTEM_OUT")
                .add(layoutComponentBuilder));

        builder.add(newRollingFileAppenderComponent(builder, "R1", "1MB", _getLogFilePath.apply("trace"), pattern, Level.TRACE, 3));
        builder.add(newRollingFileAppenderComponent(builder, "R2", _maxLogFileSize, _getLogFilePath.apply("debug"), pattern, Level.DEBUG, 3));
        builder.add(newRollingFileAppenderComponent(builder, "R3", _maxLogFileSize, _getLogFilePath.apply("info"), pattern, Level.INFO, 3));
        builder.add(newRollingFileAppenderComponent(builder, "R4", "256KB", _getLogFilePath.apply("warn"), pattern, Level.WARN, 3));
        builder.add(newRollingFileAppenderComponent(builder, "R5", "256KB", _getLogFilePath.apply("error"), pattern, Level.ERROR, 3));
        builder.add(newRollingFileAppenderComponent(builder, "R6", "256KB", _getLogFilePath.apply("fatal"), pattern, Level.FATAL, 3));
        builder.add(newRollingFileAppenderComponent(builder, "HTTPD", "1MB", _getLogFilePath.apply("httpd"), "%d{ISO8601} " + patternTail, Level.TRACE, 3));

        // configure loggers:
        List<AppenderRefComponentBuilder> appenderReferences = new ArrayList();
        appenderReferences.add(builder.newAppenderRef("R1"));
        appenderReferences.add(builder.newAppenderRef("R2"));
        appenderReferences.add(builder.newAppenderRef("R3"));
        appenderReferences.add(builder.newAppenderRef("R4"));
        appenderReferences.add(builder.newAppenderRef("R5"));
        appenderReferences.add(builder.newAppenderRef("R6"));
        appenderReferences.add(builder.newAppenderRef("HTTPD"));
        appenderReferences.add(builder.newAppenderRef("Console"));
        
        builder.add(newLoggerComponent(builder, "hex", appenderReferences));
        builder.add(newLoggerComponent(builder, "water", appenderReferences));
        builder.add(newLoggerComponent(builder, "ai.h2o", appenderReferences));
        builder.add(builder.newRootLogger(String.valueOf(L4J_LVLS[_level])).add(appenderReferences.get(appenderReferences.size() - 1)));
        
        // HTTPD logging
        builder.addProperty("log4j.logger.water.api.RequestServer", "TRACE, HTTPD");
        builder.addProperty("log4j.additivity.water.api.RequestServer", "false");

        // Turn down the logging for some class hierarchies.
        builder.addProperty("log4j.logger.org.apache.http", "WARN");
        builder.addProperty("log4j.logger.com.amazonaws", "WARN");
        builder.addProperty("log4j.logger.org.apache.hadoop", "WARN");
        builder.addProperty("log4j.logger.org.jets3t.service", "WARN");
        builder.addProperty("log4j.logger.org.reflections.Reflections", "ERROR");
        builder.addProperty("log4j.logger.com.brsanthu.googleanalytics", "ERROR");

        // Turn down the logging for external libraries that Orc parser depends on-->
        builder.addProperty("log4j.logger.org.apache.hadoop.util.NativeCodeLoader", "ERROR");
        

        Configurator.initialize(builder.build());
    }

    AppenderComponentBuilder newRollingFileAppenderComponent(ConfigurationBuilder builder, String name, String sizeBasedTriggeringPolicyValue,  String fileNameValue, String filePatternValue, Level thresholdFilterLevel, int rolloverStrategyValue) {
        ComponentBuilder triggeringPolicy = builder.newComponent("Policies")
                .addComponent(builder.newComponent("SizeBasedTriggeringPolicy").addAttribute("size", sizeBasedTriggeringPolicyValue));
        LayoutComponentBuilder layoutBuilder = builder.newLayout("PatternLayout")
                .addAttribute("pattern", filePatternValue);
        FilterComponentBuilder thresholdFilter = builder.newFilter("ThresholdFilter", Filter.Result.ACCEPT, Filter.Result.NEUTRAL)
                .addAttribute("level", L4J_LOGGING_LVLS[_level].toString());
        ComponentBuilder rolloverStrategy = builder.newComponent("DefaultRolloverStrategy").addAttribute("max", rolloverStrategyValue);

        AppenderComponentBuilder appenderBuilder = builder.newAppender(name, "RollingFile")
                .addAttribute("fileName", fileNameValue)
                .addAttribute("filePattern", fileNameValue.substring(0,fileNameValue.length() - 4) + "-%d{MM-dd-yyyy}.log.gz")
                .add(thresholdFilter)
                .addComponent(triggeringPolicy)
                .addComponent(layoutBuilder)
                .addComponent(rolloverStrategy);

        return appenderBuilder;
    }

    LoggerComponentBuilder newLoggerComponent(ConfigurationBuilder builder, String name, List<AppenderRefComponentBuilder> appenderReferences) {
        LoggerComponentBuilder loggerComponentBuilder = builder.newLogger(name);
        for (AppenderRefComponentBuilder reference : appenderReferences) {
            loggerComponentBuilder.add(reference);
        }
        loggerComponentBuilder.addAttribute("additivity", false);
        return loggerComponentBuilder;
    }
    
}
