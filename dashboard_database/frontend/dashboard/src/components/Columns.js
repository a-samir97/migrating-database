import React from 'react';
import { message, Button, Table, Popconfirm, notification } from 'antd';

const axios = require('axios').default

const deletedSucessfullyMessage = () => {
  message.success('row is deleted successfully.');
};

const deleteErrorMessage = () => {
  message.error("row is not deleted, there is an error")

}

export class ColumnsList extends React.Component {

  constructor(props){
    super(props)

    this.props.columns.push(
      {
        title: 'operation',
        dataIndex: 'operation',
        render: (text, record) =>(
            <Popconfirm title="Sure to delete?" onConfirm={() => this.DeleteRow(record)} >
              <Button danger >Delete</Button>
            </Popconfirm>
        )
      }, 
      {
        title: 'operation',
        dataIndex: 'operation',
        render: (text,record) =>
        (
            <Popconfirm title="Sure to Edit?" onConfirm={() => this.EditRow(record)}>
              <Button >Edit</Button>
            </Popconfirm>
        )
      },
    )

    this.state = {
      columns: this.props.columns,
      dataSource:this.props.data,

    }
  }

  rowSelection = {
    onChange: (selectedRowKeys, selectedRows) => {
      console.log(selectedRows, selectedRowKeys);
    },
  
    getCheckboxProps: (record) => ({
      disabled: record.name === 'Disabled User',
      // Column configuration not to be checked
      name: record.name,
    }),
  };
  
  handleDelete = (key) => {
    const dataSource = [...this.state.dataSource];
    this.setState({
      dataSource: dataSource.filter((item) => item.key !== key),
    });
  };

  DeleteRow = (record) => {
    console.log(record);
    // to delete row
    axios.delete(`http://127.0.0.1:5000/db/${this.props.tableName}/delete/${record.key+1}`)
    .then((response) => {
      // message appear after deletion
      deletedSucessfullyMessage();
      // delete record from table
      this.handleDelete(record.key);
    })
    .catch((error) => {
      deleteErrorMessage();
    })
  };

  
  EditRow = (record) => {
    // to edit row 
    axios.put('URL',{})
    .then(()=> {

    })
    .catch(() => {

    })

    console.log(record);
  };

  render(){ 
    return (
      <div>
        <Table
          rowSelection={{
            type: 'checkbox',
            ...this.rowSelection,
          }}
          columns={this.state.columns}
          dataSource={this.state.dataSource}
        />
      </div>
    );
  }
};
