import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    menuButton: {
        marginRight: theme.spacing(2),
    },
    title: {
        flexGrow: 1,
    },
}));

function renderHosts(dashboard) {
    dashboard.setState({show: "hosts"})
}

function renderDevices(dashboard) {
    dashboard.setState({show: "devices"})
}

function renderServices(dashboard) {
    dashboard.setState({show: "services"})
}

function renderCapture(dashboard) {
    dashboard.setState({show: "capture"})
}

export default function DashboardAppBar(props) {
    const classes = useStyles();
    const dashboard = props.dashboard;

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" className={classes.title} style={{paddingLeft: '20px'}}>
                        <b>hazzle Prime</b> Dashboard
                    </Typography>
                    <Button color="inherit" onClick={() => renderDevices(dashboard)}>Devices</Button>
                    <Button color="inherit" onClick={() => renderHosts(dashboard)}>Hosts</Button>
                    <Button color="inherit" onClick={() => renderServices(dashboard)}>Services</Button>
                    <Button color="inherit" onClick={() => renderCapture(dashboard)}>Capture</Button>
                </Toolbar>
            </AppBar>
        </div>
    );
}