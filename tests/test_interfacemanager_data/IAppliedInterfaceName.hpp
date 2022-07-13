#ifndef AY_FOO_BAR_IAPPLIEDINTERFACENAME_
#define AY_FOO_BAR_IAPPLIEDINTERFACENAME_

namespace ay::foo::bar {
struct IAppliedInterfaceName {
  virtual void IAppliedInterfaceName() = 0;
  virtual ~IAppliedInterfaceName(){};
  virtual void a_run() = 0;
  virtual int b_run() = 0;
  virtual void c_run() = 0;
};
}// namespace ay::foo::bar

#endif//AY_FOO_BAR_IAPPLIEDINTERFACENAME_
