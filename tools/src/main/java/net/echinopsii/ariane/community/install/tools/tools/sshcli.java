/**
 * [DEFINE YOUR PROJECT NAME/MODULE HERE]
 * [DEFINE YOUR PROJECT DESCRIPTION HERE] 
 * Copyright (C) 18/05/14 echinopsii
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

package net.echinopsii.ariane.community.install.tools.tools;

import org.apache.sshd.ClientChannel;
import org.apache.sshd.ClientSession;
import org.apache.sshd.SshClient;
import org.apache.sshd.client.future.ConnectFuture;
import org.apache.sshd.common.RuntimeSshException;

import java.io.*;

public class sshcli {

    private static  String hostname;
    private static int port;
    private static String username;
    private static String password;
    private static String commandsFilePath;

    private static File commandsFile;

    private static void parse(String[] args) {
        if (args.length==5) {
            hostname = args[0];
            port = new Integer(args[1]);
            username = args[2];
            password = args[3];
            commandsFilePath = args[4];
        } else {
            System.err.println("Error on command line arguments !");
            System.exit(-1);
        }

        commandsFile = new File(commandsFilePath);
        if (!commandsFile.isFile() || !commandsFile.canRead()) {
            System.err.println("File " + commandsFilePath + " doesn't exists or is not readable...");
            System.exit(-1);
        }
    }

    public static void main(String[] args) throws Exception {
        parse(args);

        SshClient client = SshClient.setUpDefaultClient();
        client.start();

        ClientSession session = null;
        int retries = 0;
        do {
            ConnectFuture future = client.connect(hostname, port);
            future.await();
            try {
                session = future.getSession();
            } catch (RuntimeSshException ex) {
                if (retries++ < 10) {
                    Thread.sleep(2 * 1000);
                    System.out.println("retrying connect on "+hostname+":"+port+" (attempt " + retries + ") ...");
                } else {
                    throw ex;
                }
            }
        } while (session == null);

        session.authPassword(username, password).await().isSuccess();
        System.out.println("Connected successfully !");

        ClientChannel channel = session.createChannel(ClientChannel.CHANNEL_SHELL);
        //InputStream in = new NoCloseInputStream(System.in); channel.setIn(in);
        PipedOutputStream pipedIn = new PipedOutputStream();
        InputStream in = new PipedInputStream(pipedIn); channel.setIn(in);
        ByteArrayOutputStream out = new ByteArrayOutputStream(); channel.setOut(out);
        //OutputStream out = new NoCloseOutputStream(System.out); channel.setOut(out);
        ByteArrayOutputStream err = new ByteArrayOutputStream(); channel.setErr(err);
        //OutputStream err = new NoCloseOutputStream(System.err); channel.setErr(err);
        channel.open();

        BufferedReader bf = new BufferedReader(new InputStreamReader(new FileInputStream(commandsFile)));
        String line;
        while ((line = bf.readLine())!=null) {
            System.out.println(line);
            pipedIn.write((line + "\n").getBytes());
            pipedIn.flush();
        }
        //pipedIn.write("ls\n".getBytes());
        pipedIn.write("disconnect\n".getBytes());
        pipedIn.write("\n".getBytes());

        //BufferedReader bi = new BufferedReader(new InputStreamReader(in));
        //String line;
        //while ((line = bi.readLine()) != null)

        channel.waitFor(ClientChannel.CLOSED, 0);
        channel.close(false);
        session.close(false);
        client.stop();
        //out.writeTo(System.out);
        //System.err.println(err.toByteArray().length);
        //err.writeTo(System.err);

        //out.flush();
        //err.flush();
    }
}