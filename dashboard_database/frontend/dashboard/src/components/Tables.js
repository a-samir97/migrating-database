import React from 'react'
import { Layout, Menu, Breadcrumb } from 'antd';
import  { ColumnsList }  from './Columns';

const { Header, Content, Sider } = Layout;

const axios = require('axios').default

export class Table extends React.Component {

    constructor(props){
      super(props)
      this.state = {
        collapsed: false,
        tables:[],
        columns:[],
      }
    }

    componentDidMount() {
        axios.get('http://127.0.0.1:5000/db/all-tables')
        .then( 
            (response) => {
                console.log(response.data);
                this.setState({
                  tables:response.data
                })
        })
        .catch(function (error){
            console.log(error)
        })
      }

      toggleCollapsed = () => {
        this.setState({
          collapsed: !this.state.collapsed,
        });
      };

      HandleChange = (item)=> {
        let columnName = item.key;

        // call the API by axios
        axios.get(`http://127.0.0.1:5000/db/table-details/${columnName}`)
        .then((response)=>{
            this.setState({
              columns:response.data
            })

        })
        .catch((error)=>{
          console.log(error)
        })

      }

    render(){
        let tableList = [];
        for (let i = 0; i < this.state.tables.length; i++) {
          
          tableList.push(
          <Menu.Item key={ this.state.tables[i] }>{ this.state.tables[i] }</Menu.Item> 
          )
        }
        return(
          <Layout>
          <Header className="header">
            <div className="logo" />
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['2']}>
              <Menu.Item key="1">nav 1</Menu.Item>
              <Menu.Item key="2">nav 2</Menu.Item>
              <Menu.Item key="3">nav 3</Menu.Item>
            </Menu>
          </Header>

          <Layout>
            <Sider width={200} className="site-layout-background">
              <Menu
                mode="inline"
                theme='dark'
                defaultSelectedKeys={['1']}
                defaultOpenKeys={['sub1']}
                style={{ height: '100%', borderRight: 0 }}
                onClick={this.HandleChange}
              >
                { tableList }

              </Menu>
            </Sider>
            <Layout style={{ padding: '0 24px 24px' }}>
              <Breadcrumb style={{ margin: '16px 0' }}>
                <Breadcrumb.Item>Home</Breadcrumb.Item>
                <Breadcrumb.Item>List</Breadcrumb.Item>
                <Breadcrumb.Item>App</Breadcrumb.Item>
              </Breadcrumb>
              <Content
                className="site-layout-background"
                style={{
                  padding: 24,
                  margin: 0,
                  minHeight: 280,
                }}
              >
                {
                this.state.columns.length > 1
                ?
                 <ColumnsList columns={this.state.columns}></ColumnsList>
                :
                <p>Select Table to See Columns</p>
                }
              </Content>
            </Layout>
          </Layout>
        </Layout>

        )
    }
}
