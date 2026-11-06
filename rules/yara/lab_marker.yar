rule LAB_Network_Defense_Fixture
{
  meta:
    description = "Benign local fixture marker; not a malware detector"
    author = "Network Defense Lab"
  strings:
    $fixture = "LAB_NETWORK_DEFENSE_FIXTURE" ascii
  condition:
    $fixture
}
