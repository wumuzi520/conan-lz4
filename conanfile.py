from conans import ConanFile, tools, os

class LZ4Conan(ConanFile):
    name = "LZ4"
    version = "1.8.0"
    description = "Extremely Fast Compression algorithm"
    license = "https://github.com/lz4/lz4/blob/master/lib/LICENSE"
    url = "https://github.com/bincrafters/conan-lz4"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    lib_short_name = "lz4"
    archive_name = "{0}-{1}".format(lib_short_name, version)
            
    def source(self):
        source_url = "https://github.com/lz4/lz4"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
                
    def build(self):
        if self.settings.os == "Windows":
            sln = os.path.join(self.archive_name, "visual", "vs2010", "lz4.sln")
            if self.options.shared:
                target = "liblz4-dll"
            else: 
                target = "liblz4"
            vcvars_cmd = tools.vcvars_command(self.settings)
            build_cmd = tools.msvc_build_command(self.settings, sln_path=sln , targets=[target])
            self.run("{0} && {1}".format(vcvars_cmd, build_cmd))

        #if self.settings.os == "Linux":
        #if self.settings.os == "Darwin":
       
    
    def package(self):

        # yes, headers are in lib
        include_dir = os.path.join("%s-%s" % ( self.name, self.version ), 'lib')

        self.copy(pattern="lz4*.h", dst="include", src=include_dir, keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
            
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.includedirs = ['include']