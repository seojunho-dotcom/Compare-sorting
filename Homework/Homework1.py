#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <random>
#include <iomanip>
using namespace std;
using namespace chrono;

static void merge_range(vector<int>& a, int L, int M, int R, vector<int>& aux, size_t& peak) {
    aux.resize(R - L + 1);
    peak = max(peak, aux.capacity() * sizeof(int));
    int i=L,j=M+1,k=0;
    while(i<=M && j<=R) aux[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    while(i<=M) aux[k++] = a[i++];
    while(j<=R) aux[k++] = a[j++];
    for(int t=0;t<k;++t) a[L+t]=aux[t];
}
static void merge_sort_impl(vector<int>& a,int L,int R,vector<int>& aux,size_t& peak){
    if(L>=R) return;
    int M=L+(R-L)/2;
    merge_sort_impl(a,L,M,aux,peak);
    merge_sort_impl(a,M+1,R,aux,peak);
    merge_range(a,L,M,R,aux,peak);
}
void mergeSort(vector<int>& a,size_t& extra_bytes){
    vector<int> aux; extra_bytes=0;
    if(!a.empty()) merge_sort_impl(a,0,(int)a.size()-1,aux,extra_bytes);
}

static int hoare_partition(vector<int>& a,int lo,int hi){
    int pivot=a[lo+(hi-lo)/2],i=lo-1,j=hi+1;
    while(true){
        do{++i;}while(a[i]<pivot);
        do{--j;}while(a[j]>pivot);
        if(i>=j) return j;
        swap(a[i],a[j]);
    }
}
static void quick_sort_impl(vector<int>& a,int lo,int hi){
    if(lo<hi){int p=hoare_partition(a,lo,hi); quick_sort_impl(a,lo,p); quick_sort_impl(a,p+1,hi);}
}
void quickSort(vector<int>& a){if(!a.empty()) quick_sort_impl(a,0,(int)a.size()-1);}

static void heapify(vector<int>& a,int n,int i){
    int largest=i,left=2*i+1,right=2*i+2;
    if(left<n && a[left]>a[largest]) largest=left;
    if(right<n && a[right]>a[largest]) largest=right;
    if(largest!=i){swap(a[i],a[largest]); heapify(a,n,largest);}
}
void heapSort(vector<int>& a){
    int n=(int)a.size();
    for(int i=n/2-1;i>=0;--i) heapify(a,n,i);
    for(int i=n-1;i>0;--i){swap(a[0],a[i]); heapify(a,i,0);}
}

void print_line(const vector<int>& v){for(int x:v) cout<<x<<' '; cout<<'\n';}
bool is_sorted_check(const vector<int>& a){return is_sorted(a.begin(),a.end());}

template<typename F>
void basic_test(const string& name,const vector<int>& base,F&& run){
    vector<int> a=base; size_t extra_bytes=0;
    auto t0=high_resolution_clock::now(); run(a,extra_bytes); auto t1=high_resolution_clock::now();
    auto ns=duration_cast<nanoseconds>(t1-t0).count();
    cout<<name<<" result: "; print_line(a);
    cout<<name<<" time(ns): "<<ns<<'\n';
    cout<<name<<" sorted: "<<(is_sorted_check(a)?"YES":"NO")<<'\n';
    cout<<"-----------------------------\n";
}

template<typename F>
void benchmark(const string& name,const vector<int>& base,F&& run){
    vector<int> a=base; size_t extra_bytes=0;
    auto t0=high_resolution_clock::now(); run(a,extra_bytes); auto t1=high_resolution_clock::now();
    auto ns=duration_cast<nanoseconds>(t1-t0).count();
    double data_kb=(a.capacity()*sizeof(int)+extra_bytes)/1024.0;
    cout<<left<<setw(12)<<name<<" | time: "<<setw(10)<<ns<<" ns | data: "<<fixed<<setprecision(2)<<setw(8)<<data_kb<<" KB | sorted: "<<(is_sorted_check(a)?"YES":"NO")<<'\n';
}

int main(){
    cout<<"============================================\n";
    cout<<"          BASIC SORTING TEST\n";
    cout<<"     Merge / Quick / Heap Sort\n";
    cout<<"============================================\n\n";
    vector<int> base={1,4,5,7,3,2,8};
    cout<<"Original data: "; print_line(base); cout<<'\n';
    basic_test("Merge",base,[](vector<int>& a,size_t& extra){mergeSort(a,extra);});
    basic_test("Quick",base,[](vector<int>& a,size_t& extra){quickSort(a);extra=0;});
    basic_test("Heap",base,[](vector<int>& a,size_t& extra){heapSort(a);extra=0;});
    cout<<'\n';

    cout<<"============================================\n";
    cout<<"       PERFORMANCE COMPARISON\n";
    cout<<"       n = 100 / 1,000 / 10,000\n";
    cout<<"============================================\n\n";
    vector<int> sizes={100,1000,10000};
    mt19937 rng(2026);
    uniform_int_distribution<int> dist(1,100000);
    for(int n:sizes){
        vector<int> data(n);
        for(int& x:data) x=dist(rng);
        cout<<"--------------------------------------------\n";
        cout<<"Input Size: n = "<<n<<'\n';
        cout<<"--------------------------------------------\n";
        benchmark("Merge Sort",data,[](vector<int>& a,size_t& extra){mergeSort(a,extra);});
        benchmark("Quick Sort",data,[](vector<int>& a,size_t& extra){quickSort(a);extra=0;});
        benchmark("Heap Sort",data,[](vector<int>& a,size_t& extra){heapSort(a);extra=0;});
        cout<<'\n';
    }
    cout<<"============================================\n";
    cout<<"           ALL TESTS COMPLETED\n";
    cout<<"============================================\n";
    return 0;
}
