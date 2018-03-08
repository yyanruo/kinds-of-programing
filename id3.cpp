#include <iostream>
#include <cmath>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;


const unsigned att_num = 3;
const unsigned rule_num = 14;
string decision_tree_name("Play Golf ?");
string attribute_names[] = {"Outlook", "Humidity", "Windy"};
string attribute_values[] = {"Sunny", "Overcast", "Rainy", "> 75", "<= 75", "True", "False", "Yes", "No"};
//训练集最后一列为分类标签，所以总列数为属性数加1
unsigned train_data[rule_num][att_num + 1] = {    
                    {0, 3, 6, 8},{0, 3, 5, 8},{1, 3, 6, 7},
                    {2, 3, 6, 7},{2, 3, 6, 7},{2, 4, 5, 8},
                    {1, 4, 5, 7},{0, 3, 6, 8},{0, 4, 6, 7},
                    {2, 3, 6, 7},{0, 4, 5, 7},{1, 3, 5, 7},
                    {1, 4, 6, 7},{2, 3, 5, 8}
                                };

//将vector中重复元素合并，只保留一个
template <typename T>   
vector<T> unique(vector<T> vals) 
{
    vector<T> unique_vals;
    typename vector<T>::iterator itr;
    typename vector<T>::iterator subitr;

    int flag = 0;
    while( !vals.empty() )
    {
        unique_vals.push_back(vals[0]);
        itr = vals.begin();
        subitr = unique_vals.begin() + flag;
        while ( itr != vals.end())
        {    
            if (*subitr == *itr)
                itr = vals.erase(itr);
            else
                itr++;
        }
        flag++;
    }
    return unique_vals;
}


double log2(double n)
{
    return log10(n) / log10(2.0);
}

//根据属性的取值，计算该属性的熵
double compute_entropy(vector<unsigned> v)
{
    vector<unsigned> unique_v;
    unique_v = unique(v);

    vector<unsigned>::iterator itr;
    itr = unique_v.begin();

    double entropy = 0.0;
    auto total = v.size();
    while(itr != unique_v.end())
    {
        double cnt = count(v.begin(), v.end(), *itr); 
        entropy -= cnt / total * log2(cnt / total);
        itr++;
    }
    return entropy;
}

//计算数据集中所有属性的信息增益
vector<double> compute_gain(vector<vector<unsigned> > truths)
{
    vector<double> gain(truths[0].size() - 1, 0);
    vector<unsigned> attribute_vals;
    vector<unsigned> labels;
    for(unsigned j = 0; j < truths.size(); j++)
    {
        labels.push_back(truths[j].back());
    }

    for(unsigned i = 0; i < truths[0].size() - 1; i++)//最后一列是类别标签，没必要计算信息增益
    {
        for(unsigned j = 0; j < truths.size(); j++)
        attribute_vals.push_back(truths[j][i]);

        vector<unsigned> unique_vals = unique(attribute_vals);
        vector<unsigned>::iterator itr = unique_vals.begin();
        vector<unsigned> subset;
        while(itr != unique_vals.end())
        {
            for(unsigned k = 0; k < truths.size(); k++)
            {
                if (*itr == attribute_vals[k])
                {
                    subset.push_back(truths[k].back());
                }
            }
            double A = (double)subset.size();
            gain[i] += A / truths.size() * compute_entropy(subset);
            itr++;
            subset.clear();
        }
        gain[i] = compute_entropy(labels) - gain[i];
        attribute_vals.clear();
    }
    return gain;
}

//计算数据集中所有属性的信息增益比(C4.5算法中用到)
vector<double> compute_gain_ratio(vector<vector<unsigned> > truths)
{
    vector<double> gain = compute_gain(truths);
    vector<double> entropies;
    vector<double> gain_ratio;
    
    for(unsigned i = 0; i < truths[0].size() - 1; i++)//最后一列是类别标签，没必要计算信息增益比
    {
        vector<unsigned> attribute_vals(truths.size(), 0);
        for(unsigned j = 0; j < truths.size(); j++)
        {
            attribute_vals[j] = truths[j][i];
        }
        double current_entropy = compute_entropy(attribute_vals);
        if (current_entropy)
        {
            gain_ratio.push_back(gain[i] / current_entropy);
        }
        else
            gain_ratio.push_back(0.0);
        
    }
    return gain_ratio;
}

//找出数据集中最多的类别标签
template <typename T>
T find_most_common_label(vector<vector<T> > data)
{
    vector<T> labels;
    for (unsigned i = 0; i < data.size(); i++)
    {
        labels.push_back(data[i].back());
    }
    typename vector<T>:: iterator itr = labels.begin();
    T most_common_label;
    unsigned most_counter = 0;
    while (itr != labels.end())
    {
        unsigned current_counter = count(labels.begin(), labels.end(), *itr);
        if (current_counter > most_counter)
        {
            most_common_label = *itr;
            most_counter = current_counter;
        }
        itr++;
    }
    return most_common_label;
}

//根据属性，找出该属性可能的取值
template <typename T>
vector<T> find_attribute_values(T attribute, vector<vector<T> > data)
{
    vector<T> values;
    for (unsigned i = 0; i < data.size(); i++)
    {
        values.push_back(data[i][attribute]);
    }
    return unique(values);
}

/* 
在构建决策树的过程中，如果某一属性已经考察过了
那么就从数据集中去掉这一属性，此处不是真正意义
上的去掉，而是将考虑过的属性全部标记为110，当
然可以是其他数字，只要能和原来训练集中的任意数
字区别开来即可
*/
template <typename T>
vector<vector<T> > drop_one_attribute(T attribute, vector<vector<T> > data)
{
    vector<vector<T> > new_data(data.size(),vector<T>(data[0].size() - 1, 0));
    for (unsigned i = 0; i < data.size(); i++)
    {
        data[i][attribute] = 110;
    }
    return data;
}


struct Tree{
    unsigned root;//节点属性值
    vector<unsigned> branches;//节点可能取值
    vector<Tree> children; //孩子节点
};

//递归构建决策树
void build_decision_tree(vector<vector<unsigned> > examples, Tree &tree)
{
    //第一步：判断所有实例是否都属于同一类，如果是，则决策树是单节点
    vector<unsigned> labels(examples.size(), 0);
    for (unsigned i = 0; i < examples.size(); i++)
    {
        labels[i] = examples[i].back();
    }
    if (unique(labels).size() == 1)
    {
        tree.root = labels[0];
        return;
    }

    //第二步：判断是否还有剩余的属性没有考虑，如果所有属性都已经考虑过了，
    //那么此时属性数量为0，将训练集中最多的类别标记作为该节点的类别标记
    if (count(examples[0].begin(),examples[0].end(),110) == examples[0].size() - 1)//只剩下一列类别标记
    {
        tree.root = find_most_common_label(examples);
        return;
    }
    //第三步:在上面两步的条件都判断失败后，计算信息增益，选择信息增益最大
    //的属性作为根节点,并找出该节点的所有取值

    vector<double> standard = compute_gain(examples);

    //要是采用C4.5，将上面一行注释掉，把下面一行的注释去掉即可
    //vector<double> standard = compute_gain_ratio(examples);
    tree.root = 0;
    for (unsigned i = 0; i < standard.size(); i++)
    {
        if (standard[i] >= standard[tree.root] && examples[0][i] != 110)
            tree.root  = i;
    }


    tree.branches = find_attribute_values(tree.root, examples);
    //第四步:根据节点的取值，将examples分成若干子集
    vector<vector<unsigned> > new_examples = drop_one_attribute(tree.root, examples);
    vector<vector<unsigned> > subset;
    for (unsigned i = 0; i < tree.branches.size(); i++)
    {
        for (unsigned j = 0; j < examples.size(); j++)
        {
            for (unsigned k = 0; k < examples[0].size(); k++)
            {
                if (tree.branches[i] == examples[j][k])
                    subset.push_back(new_examples[j]);
            }
        }
        // 第五步:对每一个子集递归调用build_decision_tree()函数
        Tree new_tree;
        build_decision_tree(subset,new_tree);
        tree.children.push_back(new_tree);
        subset.clear();
    }
}


//从第根节点开始，逐层将决策树输出到终端显示
void print_tree(Tree tree,unsigned depth)
{
    for (unsigned d = 0; d < depth; d++) cout << "\t";
    if (!tree.branches.empty()) //不是叶子节点
    {
        cout << attribute_names[tree.root] << endl;
        
        for (unsigned i = 0; i < tree.branches.size(); i++)
        {
            for (unsigned d = 0; d < depth + 1; d++) cout << "\t";
            cout << attribute_values[tree.branches[i]] << endl;
            print_tree(tree.children[i],depth + 2);
        }
    }
    else //是叶子节点
    {
        cout << attribute_values[tree.root] << endl;
    }
        
}


int main()
{
    vector<vector<unsigned> > rules(rule_num, vector<unsigned>(att_num + 1, 0));
    for(unsigned i = 0; i < rule_num; i++)
    {
        for(unsigned j = 0; j <= att_num; j++)
            rules[i][j] = train_data[i][j];
    }
    Tree tree;
    build_decision_tree(rules, tree);
    cout << decision_tree_name << endl;
    print_tree(tree,0);
    return 0;
}
