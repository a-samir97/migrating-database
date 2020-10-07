import React from 'react'
import { Modal, Button, Form, Input, Space } from 'antd';

const layout = {
  labelCol: {
    span: 8,
  },
  wrapperCol: {
    span: 16,
  },
};

const tailLayout = {
  wrapperCol: {
    offset: 8,
    span: 16,
  },
};


export class SearchModal extends React.Component {
 
    constructor(props){
        super(props)
        // states for this component
        this.state = {
            columns:this.props.columns,
            visible:false,
        }
    }


  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  handleOk = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  handleCancel = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  render() {
      let columNames = []
      for (let i = 0; i < this.state.columns.length - 2; i++) {
          columNames.push(
            <Form.Item
            key={ this.state.columns[i]['title'] }
            label={ this.state.columns[i]['title'] }
            name={ this.state.columns[i]['title'] }
            rules={[
            {
                message: `Please input your ${this.state.columns[i]['title'] }!`,
            },
            ]}
        >
                <Input />
        </Form.Item>
    )
          
      }
    return (
    
       <Space>    
          <Button type="danger" onClick={this.showModal}>
            Search
          </Button>

          <Modal
            title="Search"
            visible={this.state.visible}
            onOk={this.handleOk}
            onCancel={this.handleCancel}
          >
              <Form
                  {...layout}
                  name="basic"
                  initialValues={{
                      remember: true,
                  }}
                  >

                  { columNames }

                  <Form.Item {...tailLayout}>
                      <Button type="primary" htmlType="submit">
                      Search
                      </Button>
                  </Form.Item>
              </Form>
          </Modal>
        </Space>
    );
  }
}
