R__LOAD_LIBRARY(libeicsmear)


using namespace std;

void analysis(string fin)
{
  string dout = ".";
  unsigned long idx = fin.find_last_of('/');
  if (idx > 0)
      dout = fin.substr(0, idx);

  idx = fin.find(".dat");
  string fname = fin.substr(0, idx);
	
  string datfile = fin;
  string rootfile = fname + ".root";

  erhic::DisKinematics::BoundaryWarning=false;
  BuildTree(datfile, dout);

  TreeToHepMC(rootfile, dout);
}
