ansible-playbook site.yml --tags infra
sleep 5
ansible-playbook site.yml --tags clean
ansible-playbook /workspace/Lab/ansible/ansible-k8s-automate/test/setup-playbook.yml
ansible-playbook /workspace/Lab/ansible/ansible-k8s-automate/test/master-playbook.yml
ansible-playbook /workspace/Lab/ansible/ansible-k8s-automate/test/worker-playbook.yml