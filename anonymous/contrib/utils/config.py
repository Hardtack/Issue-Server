import ConfigParser
from . import DictMixin, MutableDictMixin

class Section(MutableDictMixin):
    def __init__(self, name, dict_config):
        self.name = name
        self.dict_config = dict_config

    def __repr__(self):
        return '<Section("%(name)s", %(data)s)>' % {
            'name':self.name,
            'data':repr(dict(self)),
        }

    def __getitem__(self, key):
        try:
            return self.dict_config.config.get(self.name, key)
        except ConfigParser.NoOptionError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if isinstance(value, (int, float, bool)):
            value = str(value)
        self.dict_config.config.set(self.name, key, value)

    def __delitem__(self, key):
        self.dict_config.remove_option(self.name, key)

    def keys(self):
        return self.dict_config.options(self.name)

    def getint(self, option):
        return self.dict_config.getint(self.name, option)

    def getfloat(self, option):
        return self.dict_config.getfloat(self.name, option)

    def getboolean(self, option):
        return self.dict_config.getboolean(self.name, option)

class DictionaryConfig(DictMixin):
    def __init__(self, *args, **kwargs):
        self.config = ConfigParser.SafeConfigParser(*args, **kwargs)

    def __repr__(self):
        return '<DictionaryConfig(%(data)s)>' % {
            'data':repr(dict(self)),
        }

    def defaults(self):
        return self.config.defaults()

    def sections(self):
        return self.config.sections()

    def add_section(self, section):
        self.config.add_section(section)

    def has_section(self, section):
        return self.config.has_section(section)

    def options(self, section):
        return self.config.options(section)

    def has_option(self, section, option):
        return self.config.has_option(section, option)

    def read(self, filenames):
        self.config.read(filenames)

    def readfp(self, fp, filename=None):
        if filename is None:
            self.config.readfp(fp)
        else:
            self.config.readfp(fp, filename)

    def getint(self, section, option):
        return self.config.getint(section, option)

    def getfloat(self, section, option):
        return self.config.getfloat(section, option)

    def getboolean(self, section, option):
        return self.config.getboolean(section, option)

    def items(self, section):
        return self.config.items(section)

    def set(self, section, option, value):
        self.config.set(section, option, value)

    def write(self, fileobject):
        self.config.write(fileobject)

    def remove_option(self, section, option):
        return self.config.remove_option(section, option)

    def remove_section(self, section):
        return self.config.remove_section(section)

    @property
    def optionxform(self):
        return self.config.optionxform

    @optionxform.setter
    def optionxform(self, optionxform):
        self.config.optionxform = optionxform

    def __getitem__(self, key):
        if key not in self.sections():
            raise KeyError(key)
        return Section(key, self)

    def __delitem__(self, key):
        self.remove_section(key)

    def keys(self):
        return self.sections()
